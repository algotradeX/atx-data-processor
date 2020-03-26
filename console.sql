CREATE DATABASE "atx-data";

-- Extend the database with TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- We start by creating a regular SQL table

CREATE TABLE nse_data_daily (
  timestamp TIMESTAMP PRIMARY KEY NOT NULL,
  open DOUBLE PRECISION  NOT NULL,
  close    DOUBLE PRECISION  NOT NULL,
  high    DOUBLE PRECISION  NOT NULL,
  low    DOUBLE PRECISION  NOT NULL,
  volume    DOUBLE PRECISION  NOT NULL,
  symbol VARCHAR(20) NOT NULL
);

-- This creates a hypertable that is partitioned by time
--   using the values in the `time` column.

SELECT create_hypertable('nse_data_daily', 'timestamp');

DROP TABLE "nse_data_daily";

