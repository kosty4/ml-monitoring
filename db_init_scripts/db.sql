CREATE TABLE predictions (
    userid VARCHAR(50) PRIMARY KEY,
    prediction INT NOT NULL
);

CREATE TABLE actuals (
    userid VARCHAR(50) PRIMARY KEY,
    actual INT NOT NULL
);

CREATE TABLE histogram_buckets (
    id SERIAL PRIMARY KEY,
    metric_name TEXT NOT NULL,
    metric_type TEXT NOT NULL, -- e.g., "categorical" or "continuous"
    model_version TEXT NOT NULL,
    buckets JSONB NOT NULL, -- e.g., [0.1, 0.5, 1.0, 2.0] or ["low", "medium", "hi"]
    created_at TIMESTAMPTZ DEFAULT now()
);
