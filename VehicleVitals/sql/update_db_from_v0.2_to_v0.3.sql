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

-- Fuel types table
CREATE TABLE IF NOT EXISTS "fuel_types" (
    "id"            TEXT NOT NULL,
    "name"          TEXT NOT NULL ,
    "octane_level"  INTEGER,
    "cetane_level"  INTEGER,
    PRIMARY KEY("id")
);

-- Default fuel types
INSERT INTO fuel_types (id, name, octane_level, cetane_level) VALUES
    ('B9886053-B7E4-4A01-A980-37946417A899', 'Gasoline (87 Octane)', 87, NULL),
    ('6B0AAF0C-FD66-4454-816D-DE08955E77F8', 'Diesel', NULL, 40),
    ('B3E69F89-74D7-4705-AF47-6599269A79F4', 'Biodiesel', NULL, 50),
    ('2491E84A-CCEC-4E8B-A9EE-B69428A204F0', 'Premium Gasoline', 91, NULL),
    ('96F46E7C-1CD3-4E56-B256-112FA8A996C6', 'Regular Gasoline', 85, NULL),
    ('015F2814-2BDF-48E7-B913-FDBA9389A1D7', 'Midgrade Gasoline', 89, NULL),
    ('D8B6B8B1-B8C0-4FEA-BD19-B1DC892C3B70', 'E85', 105, NULL);