-- Table for cities
CREATE TABLE IF NOT EXISTS city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    population INTEGER NOT NULL,
    region TEXT
);

-- Table for location types
CREATE TABLE IF NOT EXISTS location_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, -- Name of the location type (e.g., "Residential", "Commercial")
    max_capacity INTEGER NOT NULL, -- Maximum capacity for inhabitants or usage
    used_capacity INTEGER DEFAULT 0, -- Current used capacity
    rent REAL, -- Rent for companies operating in this location type
    maintenance_cost REAL, -- Cost of maintaining this location type
    description TEXT -- Detailed description of the location type
);

-- Updated table for locations (general-purpose nodes within a city)
CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, -- Name of the location (e.g., "Node A", "Intersection 1")
    city_id INTEGER NOT NULL, -- The city this location belongs to
    location_type_id INTEGER NOT NULL, -- The type of this location
    FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE CASCADE,
    FOREIGN KEY (location_type_id) REFERENCES location_types(id) ON DELETE CASCADE
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

-- Table for city configurations
CREATE TABLE IF NOT EXISTS city_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('easy', 'medium', 'hard')), -- Difficulty level for city generation
    residential_rate REAL NOT NULL DEFAULT 0.7, -- Rate of residential locations
    commercial_rate REAL NOT NULL DEFAULT 0.3, -- Rate of commercial locations
    max_population INTEGER NOT NULL, -- Maximum population allowed in the city
    max_locations INTEGER NOT NULL, -- Maximum number of locations allowed in the city
    max_companies INTEGER NOT NULL, -- Maximum number of companies allowed in the city
    description TEXT -- Additional details about the configuration
);