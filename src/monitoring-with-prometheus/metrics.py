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
    buckets=[0.0 ,1.0],
    labelnames=["model_version"],
)

SEASONAL_GAUGE = Gauge(
    "seasonal_gauge",
    "Gauge value of the seasonal prediction",
)


FEATURE_MONTANT = Histogram(
    "montant_feature",
    "feature example distribution",
    # buckets=[i for i in range(0, 50000, 5000)],
    labelnames=["model_version"],
)

