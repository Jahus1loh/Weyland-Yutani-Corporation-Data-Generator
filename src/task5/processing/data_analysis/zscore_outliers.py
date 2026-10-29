import numpy as np
import pandas as pd
from scipy.stats import zscore


def identify_zscore_outliers(generated_data: pd.DataFrame) -> dict:
    return {
        "total": identify_total_zscore_outliers(generated_data),
        # "each_mine": identify_each_zscore_outliers(generated_data),
    }


def identify_total_zscore_outliers(generated_data: pd.DataFrame):
    daily_total = generated_data.groupby("date")["output"].sum()
    zscores = zscore(daily_total)
    return daily_total.loc[np.abs(zscores) > 3]


def identify_each_zscore_outliers(generated_data: pd.DataFrame):
    zscores = generated_data.groupby("mine")["output"].transform(
        lambda x: zscore(x, ddof=1)
    )
    return generated_data.loc[np.abs(zscores) > 3]
