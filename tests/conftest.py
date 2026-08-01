import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import User, get_current_user, get_db_session
from lead_harvester.config import settings
from lead_harvester.models.canonical import Base, CanonicalInstitution
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft

# We must ensure we're using the test database
assert "test" in settings.test_database_url.lower(), "Test database name must contain 'test'"
assert settings.test_database_url != settings.database_url, (
    "TEST_DATABASE_URL must not match DATABASE_URL"
)

from sqlalchemy.pool import NullPool

engine = create_async_engine(settings.test_database_url, echo=False, poolclass=NullPool)


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(async_engine):
    async with async_engine.connect() as connection:
        outer_transaction = await connection.begin()
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield session
        finally:
            await session.close()
            await outer_transaction.rollback()


@pytest.fixture
def override_database_dependency(db_session):
    async def get_test_session():
        yield db_session

    app.dependency_overrides[get_db_session] = get_test_session
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_a(override_database_dependency):
    async def override_user_a():
        return User(id="reviewer_A", username="Alice", role="reviewer")

    app.dependency_overrides[get_current_user] = override_user_a
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def client_b(override_database_dependency):
    async def override_user_b():
        return User(id="reviewer_B", username="Bob", role="reviewer")

    app.dependency_overrides[get_current_user] = override_user_b
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def client_admin(override_database_dependency):
    # api/permissions.py's ROLE_PERMISSIONS grants "admin" every permission --
    # the role to use for routes gated on a permission client_a's "reviewer"
    # role doesn't hold (sectors.manage, compliance.manage, deletions.fulfil,
    # outbox.manage, audit.read).
    async def override_user_admin():
        return User(id="admin_A", username="Admin", role="admin")

    app.dependency_overrides[get_current_user] = override_user_admin
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def client_viewer(override_database_dependency):
    # The most restricted role -- only leads.read/compliance.read/
    # operations.read (see api/permissions.py's ROLE_PERMISSIONS). Useful
    # for asserting a permission-gated route correctly 403s a role that
    # holds none of the permissions it needs.
    async def override_user_viewer():
        return User(id="viewer_A", username="Viewer", role="viewer")

    app.dependency_overrides[get_current_user] = override_user_viewer
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def seeded_draft(db_session: AsyncSession):
    inst = CanonicalInstitution(
        id=uuid.uuid4(), canonical_name="Test Institution", domain="test.edu", confidence_score=99.0
    )
    brief = AccountBrief(id=uuid.uuid4(), institution_id=inst.id)
    db_session.add(brief)

    draft = OutreachDraft(
        id=uuid.uuid4(),
        brief_id=brief.id,
        target_name="Test Principal",
        target_role="Principal",
        target_contact_value="test@test.edu",
        subject_line="Hello",
        body="World",
        status=DraftStatus.GENERATED,
        version=4,
    )
    db_session.add(inst)
    db_session.add(draft)
    await db_session.commit()  # This commits the savepoint due to join_transaction_mode
    return draft
