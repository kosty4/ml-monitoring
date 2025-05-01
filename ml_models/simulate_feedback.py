"""
Simulate the feedback for the ML model by providing the actual values (from the data) 
to compare with the done predictions by the ML model for monitoring.
"""

import time

from loguru import logger
import requests
from train import load_data, parse_pandas_dtypes
from constants import SLEEP_SECONDS, NUM_TRAINING_SAMPLES

def simulate_feedback():

    df = (
        load_data("ml_models/train.csv")
        .loc[NUM_TRAINING_SAMPLES:, :]
        .reset_index(drop=True)
        .pipe(parse_pandas_dtypes)
        .assign(y_true=lambda d: d["churn"])
        .loc[:, ["user_id", "y_true"]]
    )

    logger.info(f"Simulating feedback for {len(df)} instances")


    for idx, row in df.iterrows():
        data = row.to_json()
        r = requests.post("http://localhost:8000/feedback", data=data)
        logger.info(f"instance: {idx}, feedback: {r.json()}")
        logger.info(f"Sleeping delay for {SLEEP_SECONDS} seconds")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    simulate_feedback()