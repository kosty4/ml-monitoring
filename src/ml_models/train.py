from datetime import datetime
from pathlib import Path
from typing import Union
import numpy as np

import joblib
from loguru import logger
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from prometheus_client import push_to_gateway, CollectorRegistry

from ml_models.gateway import push_gateway_observations, push_gateway_numerical_feature_training
from ml_models.constants import NUM_TRAINING_SAMPLES, PUSH_GATEWAY_URL, ML_MODEL_DIRECTORY, ML_DATA_DIRECTORY
from ml_models.utils import write_to_env

categorical_features = [
    "region",
    "tenure",
    "top_pack",
]

numerical_features = [
    "montant",
    "frequence_rech",
    "revenue",
    "arpu_segment",
    "frequence",
    "data_volume",
    "on_net",
    "orange",
    "tigo",
    "zone1",
    "zone2",
    "regularity",
    "freq_top_pack",
]

def get_bins_continious_feature(feature: pd.Series, normalize=True):

    lower_bound = feature.quantile(0.025)
    upper_bound = feature.quantile(0.975)

    feature_n_percent = feature[(feature > lower_bound) & (feature < upper_bound)]

    num_bins = 30

    counts, bin_edges = np.histogram(feature_n_percent, bins=num_bins)

    if normalize:
        counts = counts / sum(counts)

    return counts, bin_edges



def load_data(data_path: Union[str, Path]) -> pd.DataFrame:
    """Load training data"""
    logger.info(f"Loading data from: {data_path}")
    df_train = pd.read_csv(data_path)

    return (
        df_train
        .rename(dict(zip(df_train.columns, df_train.columns.str.lower())), axis=1)
        .drop(["mrg"], axis=1)
        .pipe(parse_pandas_dtypes)
    )


def parse_pandas_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Parse data types for pandas dataframe of model features"""

    return df.assign(
        region=lambda d: d["region"].astype("category"),
        tenure=lambda d: d["tenure"].astype("category"),
        montant=lambda d: d["montant"].astype("float"),
        frequence_rech=lambda d: d["frequence_rech"].astype("float"),
        revenue=lambda d: d["revenue"].astype("float"),
        arpu_segment=lambda d: d["arpu_segment"].astype("float"),
        frequence=lambda d: d["frequence"].astype("float"),
        data_volume=lambda d: d["data_volume"].astype("float"),
        on_net=lambda d: d["on_net"].astype("float"),
        orange=lambda d: d["orange"].astype("float"),
        tigo=lambda d: d["tigo"].astype("float"),
        zone1=lambda d: d["zone1"].astype("float"),
        zone2=lambda d: d["zone2"].astype("float"),
        regularity=lambda d: d["regularity"].astype("float"),
        top_pack=lambda d: d["top_pack"].astype("category"),
        freq_top_pack=lambda d: d["freq_top_pack"].astype("float"),
    )


def split_X_y(df):
    """Split train or test dataframe in X and y"""
    logger.info("Splitting dataframe in X and y")
    X = df.drop(["churn"], axis=1)
    y = df["churn"]

    return X, y


def save_model(model, timestamp):
    """Save model to a pickle file using joblib"""
    model_name = f"DecisionTree_{timestamp}"
    filename = f"{ML_MODEL_DIRECTORY}/{model_name}.pkl"

    logger.info(f"Saving model to file: {filename}")
    joblib.dump(model, filename)

    write_to_env('LATEST_ML_MODEL_ARTIFACT', filename)

    return model_name


def train_model(data_path, n_rows=NUM_TRAINING_SAMPLES):
    """Training job for a model"""

    timestamp = f"{datetime.now():%Y-%m-%dT%H-%M-%S}"
    logger.info(f"Start model training job at timestamp: {timestamp}")

    df_train = load_data(data_path).head(n_rows)
    X, y = split_X_y(df_train)

    categorical_pipeline = Pipeline([
        ("selector", ColumnTransformer([("selector", "passthrough", categorical_features)])),
        ("ohe", OneHotEncoder(handle_unknown="ignore")),
    ])

    numerical_pipeline = Pipeline([
        ("selector", ColumnTransformer([("selector", "passthrough", numerical_features)])),
        ("imputation", SimpleImputer(missing_values=pd.NA, strategy="mean"))
    ])

    pipeline = Pipeline([
        ("preprocessing", FeatureUnion([
            ("categorical_pipeline", categorical_pipeline),
            ("numerical_pipeline", numerical_pipeline),
        ])),
        ("model", DecisionTreeClassifier()),
    ])

    model = GridSearchCV(
        estimator=pipeline,
        param_grid={"model__random_state": [42]},
        scoring=["accuracy", "recall", "precision"],
        refit="accuracy",
        cv=5
    )

    logger.info("Start model fitting, this may take a while ...")
    model.fit(X, y)
    model_name = save_model(model, timestamp)

    # === Push some metrics after the ML model training ===

    # Create a CollectorRegistry
    registry = CollectorRegistry()

    # Push the observed classes during training
    push_gateway_observations(registry, y.values.tolist(), model_version=model_name)

    # TODO persis bucket definitions: Use SQL to store and version buckets ensures consistency across environments.
    _, buckets = get_bins_continious_feature(X['montant'])

    # TODO push the distributions of continious features
    push_gateway_numerical_feature_training(registry, X['montant'].values, model_version=model_name, buckets=buckets)

    # Push the collection of metrics to the push gateway in one go.
    push_to_gateway(PUSH_GATEWAY_URL, job='training_job', registry=registry)



    return model


if __name__ == "__main__":
    # print(Path.cwd())
    train_model(Path(f"{ML_DATA_DIRECTORY}/train.csv"))
