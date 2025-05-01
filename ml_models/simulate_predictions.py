"""
Simulate the ML model prediction by reading in unobserved (by the model) rows and calling the prediction endpoint 
"""

import time

from loguru import logger
import requests

from train import load_data, parse_pandas_dtypes, split_X_y
from constants import SLEEP_SECONDS, NUM_TRAINING_SAMPLES

if __name__ == "__main__":

    X, _ = (
        load_data("ml_models/train.csv")
        .loc[NUM_TRAINING_SAMPLES:, :]
        .reset_index(drop=True)
        .pipe(parse_pandas_dtypes)
        .pipe(split_X_y)
    )

    logger.info(f"Simulating {len(X)} instances")

    for i in range(len(X)):
        features = X.iloc[i].to_json()
        print('input features', features)
        r = requests.post("http://localhost:8000/predict/model", data=features)
        logger.info(f"instance: {i}, prediction: {r}")
        logger.info(f"Sleeping delay for {SLEEP_SECONDS} seconds")
        time.sleep(SLEEP_SECONDS)
