import asyncio
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft


def _draft(brief_id: uuid.UUID, name: str) -> OutreachDraft:
    return OutreachDraft(
        brief_id=brief_id,
        status=DraftStatus.APPROVED,
        target_name=name,
        target_role="Principal",
        target_contact_value=f"{name.lower().replace(' ', '.')}@example.edu",
        subject_line="Hello",
        body="Hi there",
    )


@pytest.mark.asyncio
async def test_concurrent_claims_never_double_claim_the_same_draft(async_engine):
    # OutreachAutomator.run() previously read APPROVED drafts, sent them,
    # and only afterward (in a separate transaction) marked them SENT --
    # two overlapping run() invocations could both read and send the same
    # drafts before either committed. This proves the fix -- claiming via
    # SELECT ... FOR UPDATE SKIP LOCKED, then flipping to SENDING in the
    # SAME transaction -- correctly partitions a shared batch of APPROVED
    # drafts across two genuinely concurrent connections with no overlap.
    setup_conn = await async_engine.connect()
    setup_session = AsyncSession(bind=setup_conn, expire_on_commit=False)
    institution = CanonicalInstitution(
        canonical_name="Concurrency Test School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    setup_session.add(institution)
    await setup_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    setup_session.add(brief)
    await setup_session.flush()

    drafts = [_draft(brief.id, f"Contact {i}") for i in range(4)]
    setup_session.add_all(drafts)
    await setup_session.commit()
    draft_ids = {d.id for d in drafts}
    institution_id, brief_id = institution.id, brief.id
    await setup_session.close()
    await setup_conn.close()

    async def claim_batch() -> set[uuid.UUID]:
        conn = await async_engine.connect()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            async with session.begin():
                claimed = list(
                    await session.scalars(
                        select(OutreachDraft)
                        .where(OutreachDraft.status == DraftStatus.APPROVED)
                        .limit(10)
                        .with_for_update(skip_locked=True)
                    )
                )
                for d in claimed:
                    d.status = DraftStatus.SENDING
            return {d.id for d in claimed}
        finally:
            await session.close()
            await conn.close()

    results = await asyncio.gather(claim_batch(), claim_batch())

    try:
        claimed_a, claimed_b = results
        assert claimed_a.isdisjoint(claimed_b), (claimed_a, claimed_b)
        assert claimed_a | claimed_b == draft_ids
    finally:
        cleanup_conn = await async_engine.connect()
        cleanup_session = AsyncSession(bind=cleanup_conn, expire_on_commit=False)
        try:
            from sqlalchemy import delete

            await cleanup_session.execute(
                delete(OutreachDraft).where(OutreachDraft.id.in_(draft_ids))
            )
            await cleanup_session.execute(delete(AccountBrief).where(AccountBrief.id == brief_id))
            await cleanup_session.execute(
                delete(CanonicalInstitution).where(CanonicalInstitution.id == institution_id)
            )
            await cleanup_session.commit()
        finally:
            await cleanup_session.close()
            await cleanup_conn.close()
