-- Table for cities
CREATE TABLE IF NOT EXISTS city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    population INTEGER NOT NULL,
    region TEXT
);

-- Table for streets
CREATE TABLE IF NOT EXISTS street (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city_id INTEGER NOT NULL,
    length REAL,
    FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE CASCADE
);

-- Table for companies
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sector TEXT NOT NULL,
    value REAL DEFAULT 0
);

-- Table for commercial premises
CREATE TABLE IF NOT EXISTS premise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    size REAL NOT NULL,
    rent REAL NOT NULL,
    FOREIGN KEY (street_id) REFERENCES street(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
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