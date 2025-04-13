import time
from datetime import datetime
import logging

import requests
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def flatten(xss):
    return [x for xs in xss for x in xs]


def trend_data(n_changepoints, location="spaced", noise=0.001, n_samples=36_000):
    delta = np.random.laplace(size=n_changepoints)

    t = np.linspace(0, 1, n_samples)

    if location == "random":
        s = np.sort(np.random.choice(t, n_changepoints, replace=False))
    elif location == "spaced":
        s = np.linspace(0, np.max(t), n_changepoints + 2)[1:-1]
    else:
        raise ValueError('invalid `location`, should be "random" or "spaced"')

    A = (t[:, None] > s) * 1

    k, m = 0, 0

    growth = k + A @ delta
    gamma = -s * delta
    offset = m + A @ gamma
    trend = growth * t + offset + np.random.randn(len(t)) * noise

    return (
        pd.DataFrame({"t": np.arange(0, n_samples), "value": trend}),
        delta,
    )


def seasonal_data(n_components, noise=0.001, n_samples=36_000):
    def X(t, p=365.25, n=10):
        x = 2 * np.pi * (np.arange(n) + 1) * t[:, None] / p
        return np.concatenate((np.cos(x), np.sin(x)), axis=1)

    t = np.linspace(0, 1, n_samples)
    beta = np.random.normal(size=2 * n_components)

    seasonality = X(t, 3600 / len(t), n_components) @ beta + np.random.randn(len(t)) * noise

    return (
        pd.DataFrame({"t": np.arange(0, n_samples), "value": seasonality}),
        beta,
    )


def add_anomalies(df, n_anomalies=10):
    """Add random anomalies to dataframe"""
    n_samples = len(df)
    anomaly_index_starts = np.random.randint(0, n_samples, size=n_anomalies)
    anomaly_durations = np.random.randint(10, 60, size=n_anomalies)
    anomaly_ranges = flatten([
        list(range(start, stop)) for start, stop in
        zip(anomaly_index_starts, anomaly_index_starts + anomaly_durations)
    ])

    anomaly_mask = np.zeros(n_samples, dtype="int")
    anomaly_mask[anomaly_ranges] = 1

    return df.assign(value=lambda d: np.where(anomaly_mask, d["value"] + 5, d["value"]))


def simulate_seasonality():
    np.random.seed(4)
    n_samples = 36_000
    intercept_simulated_data = 5

    df_trend, delta = trend_data(10, noise=0.5, n_samples=n_samples)
    df_seasonal, beta = seasonal_data(2, noise=0.5, n_samples=n_samples)

    # replay data from 9:00 to 19:00 local time
    today = datetime.today()
    initial_timestamp = datetime(today.year, today.month, today.day, 9, 0, 0)
    timestamps = pd.date_range(initial_timestamp, periods=n_samples, freq="s")

    simulated_data = (
        pd.DataFrame((intercept_simulated_data + df_trend["value"] + df_seasonal["value"]))
        .assign(timestamp=timestamps)
        .pipe(add_anomalies)
        .loc[lambda d: d["timestamp"] > datetime.now()]  # play simulated data from current time onwards
    )

    start_time = time.time()

    for idx, value in simulated_data["value"].items():
        data = {"prediction_id": str(idx), "prediction": value}
        requests.post("http://localhost:8000/predict/seasonal", json=data)

        logger.info(f"prediction_id: {idx}, prediction: {value}")
        time.sleep(1 - ((time.time() - start_time) % 1))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    simulate_seasonality()