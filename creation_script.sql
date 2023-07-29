CREATE TABLE nur_app.west
(
    school_id text,
    name text,
    location text,
    description text,
    year smallint,
    state_id text,
    rank_id text,
    PRIMARY KEY (school_id)
);

ALTER TABLE IF EXISTS nur_app.west
    OWNER to test;

GRANT ALL ON TABLE nur_app.west TO telrich;

CREATE TABLE nur_app.rank
(
    rank_id TEXT,
    rank TEXT,
    tuition_fess SMALLINT,
    in_state SMALLINT,
    undergrad_enrollment SMALLINT,
    PRIMARY KEY (rank_id)
);

GRANT ALL ON TABLE nur_app.west TO telrich;

CREATE TABLE nur_app.state (
    state_id TEXT,
    name TEXT,
    region TEXT,
    PRIMARY KEY (state_id)
);

GRANT ALL ON TABLE nur_app.state TO telrich