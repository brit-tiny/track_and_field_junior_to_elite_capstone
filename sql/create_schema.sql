PRAGMA foreign_keys = ON;

-- DIM ATHLETES
CREATE TABLE IF NOT EXISTS dim_athletes (
    athlete_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    dob         DATE NOT NULL,
    nat         TEXT,
    UNIQUE(name,dob)
);

-- DIM EVENTS
CREATE TABLE if NOT EXISTS dim_events (
    event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name  TEXT NOT NULL,
    gender      TEXT NOT NULL,
    event_type  TEXT,
    UNIQUE(event_name, gender)
);

-- DIM MEETS
CREATE TABLE IF NOT EXISTS dim_meets (
    meet_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    venue       TEXT NOT NULL,
    country     TEXT,
    latitude    REAL,
    longitude   REAL,
    elevation   REAL,
    is_indoor   INTEGER DEFAULT 0 CHECK(is_indoor IN (0,1))
);

--FACT PERFORMANCES
CREATE TABLE IF NOT EXISTS fact_performances (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id      INTEGER NOT NULL,
    event_id        INTEGER NOT NULL,
    meet_id         INTEGER NOT NULL,
    date            DATE NOT NULL,
    mark            REAL NOT NULL,
    wind            REAL,
    age             INTEGER,
    age_group       TEXT,
    source_file     TEXT,

    FOREIGN KEY (athlete_id)    REFERENCES dim_athletes(athlete_id),
    FOREIGN KEY (event_id)      REFERENCES dim_events(event_id),
    FOREIGN KEY (meet_id)       REFERENCES dim_meets(meet_id)
);