import pandas as pd
from processing.data_analysis.helper_funcs import calculate_distance


def identify_distance_outliers(
    generated_data: pd.DataFrame, threshold: float
) -> pd.DataFrame:
    return generated_data.loc[
        calculate_distance(generated_data, "output") > threshold
    ]
