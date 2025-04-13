CREATE TABLE predictions (
    userid VARCHAR(50) PRIMARY KEY,
    prediction INT NOT NULL
);

CREATE TABLE actuals (
    userid VARCHAR(50) PRIMARY KEY,
    actual INT NOT NULL
);