import tomllib
from pathlib import Path

import pandas as pd
from structures.data_types import OutlierResult

with Path("src/task5/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    weekdays = cfg["general"]["weekdays"]


def calculate_daily_total(generated_data: pd.DataFrame) -> pd.DataFrame:
    return generated_data.groupby("date", as_index=False)["output"].sum()


def add_weekday(generated_data: pd.DataFrame) -> pd.DataFrame:
    result = generated_data.copy()
    result["weekday"] = pd.to_datetime(result["date"]).dt.day_name()
    return result


def calculate_weekday_average(
    generated_data: pd.DataFrame, value_col: str
) -> pd.DataFrame:
    weekday_data = add_weekday(generated_data)
    averages = weekday_data.groupby("weekday")[value_col].mean()
    return averages.reindex(weekdays).rename("average_output").reset_index()


def calculate_distance(
    generated_data: pd.DataFrame, value_col: str
) -> pd.Series:
    return (generated_data[value_col] - generated_data[value_col].mean()).abs()


def to_frame(outliers: OutlierResult, data: pd.DataFrame) -> pd.DataFrame:
    if isinstance(outliers, dict):
        outliers = next(iter(outliers.values()))
    if isinstance(outliers, pd.Series):
        outliers = data.loc[outliers.index]
    return outliers


def get_max_distance(generated_data: pd.DataFrame, value_col: str) -> float:
    return float(calculate_distance(generated_data, value_col).max())


def get_mine_data(generated_data: pd.DataFrame, mine: str) -> pd.DataFrame:
    return (
        generated_data.loc[generated_data["mine"] == mine]
        .sort_values("date")
        .copy()
    )
