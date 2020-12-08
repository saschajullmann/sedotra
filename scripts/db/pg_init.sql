    CREATE USER sedotra_test with password 'sedotra_test';
    CREATE DATABASE sedotra_test;
    GRANT ALL PRIVILEGES ON DATABASE sedotra_test TO sedotra_test;

    -- connect to each database and activate uuid extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    \connect sedotra_test;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";