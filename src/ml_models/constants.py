# Amount of seconds between simulating the next prediction / observation
SLEEP_SECONDS = 1
NUM_TRAINING_SAMPLES = 100_000

# Location where to store the trained artifacts
ML_MODEL_DIRECTORY = './src/ml_models/artifacts'

ML_DATA_DIRECTORY = './src/ml_models/data'

# Prometheus Push Gateway URL
PUSH_GATEWAY_URL = 'localhost:9091'