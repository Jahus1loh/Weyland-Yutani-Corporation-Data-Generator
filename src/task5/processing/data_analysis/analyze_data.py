from collections.abc import Mapping
from typing import Any

import pandas as pd
from processing.data_analysis.basic_stats import (
    calculate_mean_std_median,
)
from processing.data_analysis.distance import identify_distance_outliers
from processing.data_analysis.grubbs import identify_grubbs_outliers
from processing.data_analysis.iqr_outliers import (
    calculate_iqr,
    identify_iqr_outliers,
)
from processing.data_analysis.zscore_outliers import (
    identify_zscore_outliers,
)
from structures.data_types import OutlierResult


def analyze_data(generated_data: pd.DataFrame) -> Mapping[str, Any]:
    daily_output_basic_stats = calculate_mean_std_median(generated_data)
    daily_output_iqr = calculate_iqr(generated_data)
    outliers = identify_outliers(generated_data, distance_threshold=1)
    return {
        "basic_stats": daily_output_basic_stats,
        "iqr": daily_output_iqr,
        "outliers": outliers,
    }


def identify_outliers(
    generated_data: pd.DataFrame, distance_threshold: float
) -> Mapping[str, OutlierResult]:
    return {
        "iqr_outliers": identify_iqr_outliers(generated_data),
        "z_score_outliers": identify_zscore_outliers(generated_data),
        "grubbs": identify_grubbs_outliers(generated_data),
        "distance": identify_distance_outliers(
            generated_data, distance_threshold
        ),
    }
