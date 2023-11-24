-- Version table
CREATE TABLE IF NOT EXISTS "version" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "schema_version" INTEGER NOT NULL
);

-- configurations table
CREATE TABLE IF NOT EXISTS "configurations" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "key" TEXT NOT NULL,
    "value" TEXT,
    UNIQUE ("key")
);