from collections.abc import Mapping

import pandas as pd


def identify_iqr_outliers(
    generated_data: pd.DataFrame,
) -> Mapping[str, pd.DataFrame]:
    return {
        "total_outliers": mark_iqr_outliers(generated_data),
    }


def find_total_lower_and_upper_iqr_bounds(
    generated_data: pd.DataFrame, iqr: float
) -> tuple[float, float]:
    data_to_check = generated_data
    if isinstance(generated_data, pd.DataFrame):
        data_to_check = generated_data["output"]
    q1, q3 = data_to_check.quantile([0.25, 0.75])
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def mark_iqr_outliers(generated_data: pd.DataFrame) -> pd.DataFrame:
    iqr = calculate_iqr(generated_data)
    daily_total = generated_data.groupby("date")["output"].sum()
    lower, upper = find_total_lower_and_upper_iqr_bounds(daily_total, iqr)
    mask = (daily_total < lower) | (daily_total > upper)
    return daily_total[mask]


def calculate_iqr(daily_total: pd.DataFrame) -> float:
    quartiles = daily_total["output"].quantile([0.25, 0.75])
    iqr = quartiles[0.75] - quartiles[0.25]
    return iqr
