from collections.abc import Mapping
from typing import Any

import pandas as pd


def calculate_mean_std_median(
    generated_data: pd.DataFrame,
) -> Mapping[str, Any]:
    total_mines_stats = calculate_total_mean_std_median(generated_data)
    return {
        "total_stats": total_mines_stats,
    }


def calculate_total_mean_std_median(
    generated_data: pd.DataFrame,
) -> pd.DataFrame:
    daily_total = generated_data.groupby("date")["output"].sum()
    total_mines_stats = daily_total.agg(["mean", "std", "median"])
    return total_mines_stats
