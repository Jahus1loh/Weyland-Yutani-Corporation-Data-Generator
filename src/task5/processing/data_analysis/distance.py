import pandas as pd


def identify_distance_outliers(
    generated_data: pd.DataFrame,
    threshold: float,
) -> pd.DataFrame:
    distance = (
        generated_data["output"] - generated_data["output"].mean()
    ).abs()
    return generated_data.loc[distance > threshold]
