-- Add a new column to the logs table
ALTER TABLE logs
ADD COLUMN service_type_id TEXT;

-- parts table
CREATE TABLE IF NOT EXISTS "parts" (
    "id"            TEXT NOT NULL,
    "name"          TEXT,
    "description"   TEXT,
    "cost"          REAL,
    PRIMARY KEY("id")
);

-- service_types table
CREATE TABLE IF NOT EXISTS "service_types" (
    "id"            TEXT NOT NULL,
    "name"          TEXT,
    "description"   TEXT,
    "interval_days" INTEGER,
    "interval_miles" INTEGER,
    PRIMARY KEY("id")
);

-- service_type_parts table (junction table)
CREATE TABLE IF NOT EXISTS "service_type_parts" (
    "service_type_id" TEXT NOT NULL,
    "part_id"         TEXT NOT NULL,
    PRIMARY KEY("service_type_id", "part_id"),
    FOREIGN KEY ("service_type_id") REFERENCES "service_types" ("id"),
    FOREIGN KEY ("part_id") REFERENCES "parts" ("id")
);

-- Create service types for distinct services
INSERT OR IGNORE INTO service_types (id, name, description, interval_days, interval_miles)
VALUES
    ('03EB0F23-65B6-446D-8AED-7BBE42367362', 'Engine Oil', 'Engine oil change', 30, 3000),
    ('1C53EFD2-EE43-4E93-AC48-B5A2BF37C909', 'Fuel Filter', 'Replace fuel filter', 90, 9000),
    ('E0322B94-F60F-4610-AD44-66CEA8578A9D', 'Air Filter', 'Replace air filter', 60, 6000),
    ('0768AC11-11CB-46C2-8008-6CEE22AF0330', 'Cabin Air Filter', 'Replace cabin air filter', 180, 18000);

-- Update the service_type_id in the logs table based on the service names
UPDATE logs
SET service_type_id = (
    SELECT id
    FROM service_types
    WHERE name = logs.services
);
