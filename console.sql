CREATE DATABASE "atx-data";

-- Extend the database with TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- We start by creating a regular SQL table

CREATE TABLE nec_data (
  time        TIMESTAMPTZ       NOT NULL,
  open DOUBLE PRECISION  NOT NULL,
  close    DOUBLE PRECISION  NOT NULL,
  high    DOUBLE PRECISION  NOT NULL,
  low    DOUBLE PRECISION  NOT NULL,
  volume    DOUBLE PRECISION  NOT NULL
);

-- This creates a hypertable that is partitioned by time
--   using the values in the `time` column.

SELECT create_hypertable('nec_data', 'time');

