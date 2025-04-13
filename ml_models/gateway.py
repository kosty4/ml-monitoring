import requests

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Histogram, pushadd_to_gateway

# # Create a Gauge metric
# gauge = Gauge('example_metric', 'Example metric pushed to Push Gateway', labelnames=['label_name'], registry=registry)



# # Set the metric value
# gauge.labels(label_name='example_label').set(42)

# # Push the metric to the Push Gateway
# # Use pushadd_to_gateway if you want to add or replace metrics with the same name.
# push_to_gateway(push_gateway_url, job='example_job', registry=registry)


def push_gateway_observations(observations):
    # observations = [0, 0, 0, 0, 1.0]

    # Define the Prometheus Push Gateway URL
    push_gateway_url = 'localhost:9091'

    # Create a CollectorRegistry
    registry = CollectorRegistry()

    # Create a Histogram metric
    histogram = Histogram('training_histogram', 'Example histogram pushed to Push Gateway', buckets=[0.0, 1.0], registry=registry)

    # Observe values in the histogram
    for value in observations:
        histogram.observe(value)

    # Push the histogram to the Push Gateway
    push_to_gateway(push_gateway_url, job='training_job', registry=registry)

    # out = {'churn' : 123, 'no_churn': 172}

    # requests.post('http://localhost:9091/metrics/job/metricfire/instance/article', data= observations.json())

def push_gateway_numerical_feature_training(buckets, counts):
    """
    buckets:
    """

    # Define the Prometheus Push Gateway URL
    push_gateway_url = 'localhost:9091'

    # Create a CollectorRegistry
    registry = CollectorRegistry()

    # Create a Histogram metric
    histogram = Histogram('montant_training', 'montant feature observed during training', buckets=buckets, registry=registry)

    for i in counts:
        histogram.observe(i)

    # Push the histogram to the Push Gateway
    push_to_gateway(push_gateway_url, job='drift_detection_job', registry=registry)

