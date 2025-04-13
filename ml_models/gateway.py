import requests

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Histogram, Counter, pushadd_to_gateway

from constants import PUSH_GATEWAY_URL


def push_gateway_observations(observations):
    # observations = [0, 0, 0, 0, 1.0]

    # Create a CollectorRegistry
    registry = CollectorRegistry()

    counter = Counter(
        "training_counter",
        "Class distribution of training samples",
        labelnames=["observed_class"],
        registry=registry
    )


    # Observe values into the counter
    for value in observations:
        counter.labels(observed_class=str(value)).inc()

    # Push the histogram to the Push Gateway
    push_to_gateway(PUSH_GATEWAY_URL, job='training_job', registry=registry)

# TODO
def push_gateway_numerical_feature_training(buckets, counts):
    """
    buckets:
    """

    # Create a CollectorRegistry
    registry = CollectorRegistry()

    # Create a Histogram metric
    histogram = Histogram('montant_training', 'montant feature observed during training', buckets=buckets, registry=registry)

    for i in counts:
        histogram.observe(i)

    # Push the histogram to the Push Gateway
    push_to_gateway(PUSH_GATEWAY_URL, job='drift_detection_job', registry=registry)

