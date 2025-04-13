import requests

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Histogram, pushadd_to_gateway

from constants import PUSH_GATEWAY_URL
# # Create a Gauge metric
# gauge = Gauge('example_metric', 'Example metric pushed to Push Gateway', labelnames=['label_name'], registry=registry)

def push_gateway_observations(observations):
    # observations = [0, 0, 0, 0, 1.0]

    # Create a CollectorRegistry
    registry = CollectorRegistry()

    # Create a Histogram metric
    histogram = Histogram('training_histogram', 'Example histogram pushed to Push Gateway', buckets=[0.0, 1.0], registry=registry)

    # Observe values in the histogram
    for value in observations:
        histogram.observe(value)

    # Push the histogram to the Push Gateway
    push_to_gateway(PUSH_GATEWAY_URL, job='training_job', registry=registry)

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

