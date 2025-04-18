import asyncio
import random
import time

import numpy as np
import joblib
import asyncio


from fastapi import FastAPI

from fastapi.responses import PlainTextResponse

from prometheus_client import Counter, generate_latest, Histogram, Gauge

from pydantic import BaseModel

import pandas as pd

from .metrics import REQUEST_COUNT, REQUEST_LATENCY, REQUEST_ERROR, RESPONSE_DIST, PREDICT_COUNTER, \
    SEASONAL_GAUGE, FEATURE_MONTANT

from .db_manager import DB_CREDENTIALS, DatabaseManager
from .models import Seasonal, Features, Feedback, parse_pandas_dtypes

# from prometheus_async.aio import time


db_creds = DB_CREDENTIALS(dbname='monitoring_db', user='postgres', password='postgres', host='postgres', port=5432)
db_conn = DatabaseManager(credentials=db_creds)

app = FastAPI()


# Load prediction model  == ML Monitoring imports
MODEL_VERSION = "./monitoring-with-prometheus/DecisionTree_2025-04-13T11-43-06"
model = joblib.load(f"{MODEL_VERSION}.pkl")


traffic_count = Counter("traffic_count", documentation="Counter for counting visits")

error_counter = Counter('error_count', "Error counter")

with error_counter.count_exceptions(ValueError):
    error_counter.inc()


latency_histogram = Histogram('latency_histogram', 'Description of histogram')



@app.get("/")
def root():
    return "Hello world"


@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    
    return generate_latest()


# Get a random number when visiting this endpoint
@app.get("/random")
@latency_histogram.time()
# @error_counter.count_exceptions()
def get_random(sleep_time_max = 5): #note -> divided by 10
    traffic_count.inc()


    # We are doing some computation
    sleep_time = random.uniform(1,sleep_time_max) / 10


    # Some computation fails
    if sleep_time < 0.2:
        error_counter.inc()
        # raise ValueError

    # FastAPI is synchronous unless defined differently
    time.sleep( sleep_time )


    # latency_histogram.observe(sleep_time)

    
    return random.uniform(0,100)


@app.post("/predict/seasonal")
def post_seasonal_prediction(seasonal: Seasonal) -> Seasonal:
    """Post a seasonal prediction"""
    SEASONAL_GAUGE.set(seasonal.prediction)
    return seasonal



# New --- ML Monitoring


@app.get("/predict/random")
# @time(REQUEST_LATENCY.labels(model_version="random"))  # async time functionality
async def get_random_prediction(time_delay_scale: float = 0.1, error_rate: float = 0.01) -> float:
    """Get a random uniform prediction with an exponential time delay"""
    REQUEST_COUNT.labels(model_version="random").inc()

    time_delay = np.random.exponential(time_delay_scale)
    await asyncio.sleep(time_delay)

    if np.random.uniform() < error_rate:
        REQUEST_ERROR.labels(model_version="random").inc()
        raise ValueError("Could not make a prediction")

    prediction = np.random.uniform()
    RESPONSE_DIST.labels(model_version="random").observe(prediction)

    return prediction


@app.post("/predict/model")
@REQUEST_LATENCY.labels(model_version=MODEL_VERSION).time()
def post_model_prediction(features: Features) -> int:
    """
    Given an observation with input features, get a prediction from the deployed model
    """
    REQUEST_COUNT.labels(model_version=MODEL_VERSION).inc()

    X = pd.DataFrame().from_dict(features.dict(), orient="index").T
    X = parse_pandas_dtypes(X)

    #Peform the prediction
    prediction = str(model.predict(X).item())

    PREDICT_COUNTER.labels(model_version=MODEL_VERSION, predicted_class=prediction).inc()

    # Data Drift Monitoring
    #Track the montant feature
    # FEATURE_MONTANT.set(X.montant)
    FEATURE_MONTANT.labels(model_version=MODEL_VERSION).observe(features.montant)

    # Save the prediction to an SQL table for ML Model performance analysis
    db_conn.add_prediction(userid=features.user_id, value=prediction)


    return prediction


# ML Model Feedback
@app.post("/feedback")
def post_feedback(feedback: Feedback) -> Feedback:
    """Post the `y_true` for the `user_id` in the feedback system"""
    # Add the feedback to an SQL DB for model Performance analysis
    db_conn.add_actual(userid=feedback.user_id, value=str(feedback.y_true))

    return feedback
