CREATE DATABASE hiringdb;
-- \c hiringdb
CREATE TABLE IF NOT EXISTS candidates(
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(30),
    skills TEXT,
    education TEXT,
    experience_years INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
