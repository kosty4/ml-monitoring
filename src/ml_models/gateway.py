
from prometheus_client import Histogram, Counter


def push_gateway_observations(collection_registry, observations, model_version):

    counter = Counter(
        name="training_counter",
        documentation="Class distribution of training samples",
        labelnames=["model_version", "observed_class"],
        registry=collection_registry
    )

    # Observe values into the counter
    for value in observations:
        counter.labels(model_version=model_version, observed_class=str(value)).inc()

# TODO
def push_gateway_numerical_feature_training(collection_registry, feature_values, model_version, buckets):

    # TODO This is a copy-paste. Improve the project structure!
    hist_feature = Histogram(
        name="montant_feature_training",
        documentation="feature montant distribution",
        labelnames=["stage", "model_version"],
        buckets=buckets,
        registry=collection_registry
    )

    # buckets=[i for i in range(0, 50000, 5000)],
    
    for val in feature_values:
        hist_feature.labels(model_version=model_version, stage="training").observe(val)
