-- Create the database

CREATE DATABASE mobispace;

-- Connect to the mobispcace database
\c mobispace;

-- Create the tables
CREATE TABLE processed_data (
    id SERIAL PRIMARY KEY,
    data TEXT
);

CREATE TABLE classification_results (
    id SERIAL PRIMARY KEY,
    result TEXT
);

CREATE TABLE stop_events (
    id SERIAL PRIMARY KEY,
    event TEXT
);
