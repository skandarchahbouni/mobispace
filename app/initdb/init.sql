DROP TABLE IF EXISTS gps;
DROP TABLE IF EXISTS measures;


CREATE TABLE IF NOT EXISTS gps (
    participant_virtual_id BIGINT NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    lat DECIMAL(10,7) NOT NULL,
    lon DECIMAL(10,7) NOT NULL,
    PRIMARY KEY (participant_virtual_id, timestamp)
);

CREATE TABLE IF NOT EXISTS measures (
    participant_virtual_id INT,
    time TIMESTAMP,
    PM2_5 INT,
    PM10 INT,
    PM1_0 INT,
    Temperature FLOAT,
    Humidity FLOAT,
    NO2 FLOAT,
    BC FLOAT,
    activity VARCHAR(255),
    event VARCHAR(255)
);