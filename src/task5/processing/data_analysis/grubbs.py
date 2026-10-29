import pandas as pd
from outliers import smirnov_grubbs as grubbs


def identify_grubbs_outliers(generated_data: pd.DataFrame) -> dict:
    return {
        "total": identify_total_grubbs_outliers(generated_data),
    }


def identify_total_grubbs_outliers(
    generated_data: pd.DataFrame,
) -> pd.DataFrame:
    values = generated_data.groupby("date")["output"].sum()
    indices = grubbs.max_test_indices(
        values.tolist()
    ) + grubbs.min_test_indices(values.tolist())
    return generated_data.loc[generated_data.index.isin(indices)]
