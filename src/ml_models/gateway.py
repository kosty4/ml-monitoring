
from api.metrics import TRAINING_COUNTER, FEATURE_MONTANT

def push_gateway_observations(collection_registry, observations, model_version):

    collection_registry.register(TRAINING_COUNTER)

    # Observe values into the counter
    for value in observations:
        TRAINING_COUNTER.labels(model_version=model_version, observed_class=str(value)).inc()
    

def push_gateway_numerical_feature_training(collection_registry, feature_values, model_version, buckets):

    collection_registry.register(FEATURE_MONTANT)

    # TODO Think of a way to be able to register the buckets 
    # hist_feature = Histogram(
    #     name="montant_feature",
    #     documentation="feature montant distribution",
    #     labelnames=["stage", "model_version"],
    #     buckets=buckets,
    #     registry=collection_registry
    # )

    for val in feature_values:
        FEATURE_MONTANT.labels(model_version=model_version, stage="training").observe(val)
