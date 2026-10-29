import tomllib
from pathlib import Path

import pandas as pd

with Path("src/task5/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    weekdays = cfg["general"]["weekdays"]


def calculate_weekday_average(
    data: pd.DataFrame,
    value_col: str,
) -> pd.DataFrame:
    result = data.copy()
    result["weekday"] = pd.to_datetime(result["date"]).dt.day_name()
    return (
        result.groupby("weekday")[value_col]
        .mean()
        .reindex(weekdays)
        .rename("average_output")
        .reset_index()
    )
