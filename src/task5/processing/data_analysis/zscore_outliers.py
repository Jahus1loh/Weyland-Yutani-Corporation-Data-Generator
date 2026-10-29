from collections.abc import Mapping

import numpy as np
import pandas as pd
from scipy.stats import zscore


def identify_zscore_outliers(
    generated_data: pd.DataFrame,
) -> Mapping[str, pd.DataFrame]:
    return {
        "total": mark_zscore_outliers(generated_data),
    }


def mark_zscore_outliers(generated_data: pd.DataFrame) -> pd.DataFrame:
    daily_total = generated_data.groupby("date")["output"].sum()
    zscores = zscore(daily_total)
    return daily_total.loc[np.abs(zscores) > 3]
