from prometheus_client import Counter, Gauge, Histogram


traffic_count = Counter("traffic_count", documentation="Counter for counting visits")

error_counter = Counter('error_count', "Error counter")

with error_counter.count_exceptions(ValueError):
    error_counter.inc()


latency_histogram = Histogram('latency_histogram', 'Description of histogram')



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

TRAINING_COUNTER = Counter(
    name="training_counter",
    documentation="Class distribution of training samples",
    labelnames=["model_version", "observed_class"],
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


# Example of a continious feature
FEATURE_MONTANT = Histogram(
    name="montant_feature",
    documentation="montant feature distribution",
    labelnames=["stage", "model_version"],
)

