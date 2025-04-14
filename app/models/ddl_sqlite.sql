-- Table for cities
CREATE TABLE IF NOT EXISTS city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    population INTEGER NOT NULL,
    region TEXT
);

-- Table for locations (general-purpose nodes within a city)
CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, -- Name of the location (e.g., "Node A", "Intersection 1")
    city_id INTEGER NOT NULL, -- The city this location belongs to
    type TEXT NOT NULL, -- Type of location (e.g., "junction", "residential", "commercial")
    FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE CASCADE
);

-- Updated table for streets to connect locations
CREATE TABLE IF NOT EXISTS street (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city_id INTEGER NOT NULL,
    start_location_id INTEGER NOT NULL, -- Starting location of the street
    end_location_id INTEGER NOT NULL, -- Ending location of the street
    length REAL, -- Length of the street
    FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE CASCADE,
    FOREIGN KEY (start_location_id) REFERENCES location(id) ON DELETE CASCADE,
    FOREIGN KEY (end_location_id) REFERENCES location(id) ON DELETE CASCADE
);

-- Table for companies
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sector TEXT NOT NULL,
    value REAL DEFAULT 0
);

-- Table for employees
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL,
    company_id INTEGER NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

-- Table for customers
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE CASCADE
);

-- Table for transactions
CREATE TABLE IF NOT EXISTS sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount REAL NOT NULL,
    company_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
);

-- Table for vehicles
CREATE TABLE IF NOT EXISTS vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    type TEXT NOT NULL, -- For example: motorcycle, car, truck
    capacity REAL NOT NULL, -- Load capacity in kg
    company_id INTEGER NOT NULL,
    driver_id INTEGER, -- Relation to the employee who drives the vehicle
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES employee(id) ON DELETE SET NULL
);