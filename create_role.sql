-- Drop if exists (optional, safely handled by checking)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'opportunity_test') THEN

      CREATE ROLE opportunity_test WITH LOGIN PASSWORD 'TEST_PASSWORD' NOSUPERUSER NOCREATEDB NOCREATEROLE;
   END IF;
END
$do$;

-- Can't create database in a transaction or DO block, so just execute it.
-- We can ignore errors if it exists.
