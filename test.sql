PRAGMA foreign_keys = OFF; -- Disable foreign key constraints temporarily

-- Generate and execute DELETE statements for all user tables
BEGIN TRANSACTION;

-- Dynamically generate DELETE statements for each table
SELECT 'DELETE FROM "' || name || '";'
FROM sqlite_master
WHERE type = 'table' AND name NOT LIKE 'sqlite_%';

-- Execute each DELETE statement (manually or programmatically in your script)

COMMIT;

PRAGMA foreign_keys = ON; -- Re-enable foreign key constraints