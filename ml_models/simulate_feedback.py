"""
Simulate the feedback for the ML model by providing the actual values (from the data) 
to compare with the done predictions by the ML model for monitoring.
"""

import time

from loguru import logger
import requests

# from monitoring.train import load_data, parse_pandas_dtypes
from train import load_data, parse_pandas_dtypes


SLEEP_SECONDS = 1


def simulate_feedback():

    df = (
        load_data("ml_models/train.csv")
        .loc[100_000:, :]
        .reset_index(drop=True)
        .pipe(parse_pandas_dtypes)
        .assign(y_true=lambda d: d["churn"])
        .loc[:, ["user_id", "y_true"]]
    )

    logger.info(f"Simulating feedback for {len(df)} instances")
    logger.info(f"Sleeping delay for {SLEEP_SECONDS} seconds")
    time.sleep(SLEEP_SECONDS)

    for idx, row in df.iterrows():
        data = row.to_json()
        r = requests.post("http://localhost:8000/feedback", data=data)
        logger.info(f"instance: {idx}, feedback: {r.json()}")
        time.sleep(0.1)


if __name__ == "__main__":
    simulate_feedback()