from typing import Union
from pydantic import BaseModel

import pandas as pd

class Seasonal(BaseModel):
    prediction_id: str
    prediction: float

class Features(BaseModel):
    user_id: str
    region: Union[str, None]
    tenure: Union[str, None]
    montant: Union[float, None]
    frequence_rech: Union[float, None]
    revenue: Union[float, None]
    arpu_segment: Union[float, None]
    frequence: Union[float, None]
    data_volume: Union[float, None]
    on_net: Union[float, None]
    orange: Union[float, None]
    tigo: Union[float, None]
    zone1: Union[float, None]
    zone2: Union[float, None]
    regularity: Union[float, None]
    top_pack: Union[str, None]
    freq_top_pack: Union[float, None]


class Feedback(BaseModel):
    user_id: str
    y_true: int


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