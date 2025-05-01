from prometheus_client import Counter, Gauge, Histogram


REQUEST_COUNT = Counter(
    "request_count",
    "Total number of requests",
    labelnames=["model_version"]
)

REQUEST_ERROR = Counter(
    "request_error",
    "Total number or errors in the requests",
    labelnames=["model_version"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Time spent processing request in seconds",
    labelnames=["model_version"]
)

RESPONSE_DIST = Histogram(
    "response_distribution",
    "Response distribution of the predictions",
    labelnames=["model_version"],
)

PREDICT_COUNTER = Counter(
    "prediction_counter",
    "Class distribution of predictions",
    labelnames=["model_version", "predicted_class"],
)

SEASONAL_GAUGE = Gauge(
    "seasonal_gauge",
    "Gauge value of the seasonal prediction",
)


FEATURE_MONTANT = Histogram(
    name="montant_feature",
    documentation="feature example distribution",
    labelnames=["stage", "model_version"],
    # buckets=[i for i in range(0, 50000, 5000)],
)

