import asyncio

import asyncpg


async def main():
    # Connect to default postgres database to create the role and test db
    try:
        conn = await asyncpg.connect(
            "postgresql://postgres:development-only@127.0.0.1:5432/postgres"
        )

        # Create role
        try:
            await conn.execute(
                "CREATE ROLE opportunity_test WITH LOGIN PASSWORD 'TEST_PASSWORD' NOSUPERUSER NOCREATEDB NOCREATEROLE;"
            )
            print("Role created.")
        except asyncpg.exceptions.DuplicateObjectError:
            print("Role already exists.")

        # Create database
        try:
            await conn.execute("CREATE DATABASE lead_harvester_test OWNER opportunity_test;")
            print("Database created.")
        except asyncpg.exceptions.DuplicateDatabaseError:
            print("Database already exists.")

        await conn.close()

        # Connect to the new database to add extensions
        conn_test = await asyncpg.connect(
            "postgresql://postgres:development-only@127.0.0.1:5432/lead_harvester_test"
        )
        await conn_test.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        await conn_test.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        await conn_test.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
        print("Extensions created.")

        await conn_test.close()
    except Exception as e:
        print(f"Error setting up database: {e}")


if __name__ == "__main__":
    asyncio.run(main())
