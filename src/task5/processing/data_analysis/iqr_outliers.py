import pandas as pd


def identify_iqr_outliers(generated_data: pd.DataFrame):
    return {
        "total_outliers": identify_total_iqr_outliers(generated_data),
        # "each_outliers": identify_each_iqr_outliers(generated_data),
    }


def find_total_lower_and_upper_iqr_bounds(
    generated_data: pd.DataFrame, iqr: float
):
    data_to_check = generated_data
    if isinstance(generated_data, pd.DataFrame):
        data_to_check = generated_data["output"]
    q1, q3 = data_to_check.quantile([0.25, 0.75])
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def identify_total_iqr_outliers(generated_data: pd.DataFrame):
    iqr = calculate_total_iqr(generated_data)
    daily_total = generated_data.groupby("date")["output"].sum()
    lower, upper = find_total_lower_and_upper_iqr_bounds(daily_total, iqr)
    mask = (daily_total < lower) | (daily_total > upper)
    return daily_total[mask]


def identify_each_iqr_outliers(generated_data: pd.DataFrame):
    each_iqr = calculate_each_iqr(generated_data)
    q = (
        generated_data.groupby("mine")["output"]
        .quantile([0.25, 0.75])
        .unstack()
    )
    bounds = pd.DataFrame(
        {
            "lower": q[0.25] - 1.5 * each_iqr,
            "upper": q[0.75] + 1.5 * each_iqr,
        }
    )
    df = generated_data.join(bounds, on="mine")
    mask = (df["output"] < df["lower"]) | (df["output"] > df["upper"])
    return generated_data[mask]


def calculate_iqrs(generated_data: pd.DataFrame):
    each_iqr = calculate_each_iqr(generated_data)
    total_iqr = calculate_total_iqr(generated_data)
    return {"each_iqr": each_iqr, "total_iqr": total_iqr}


def calculate_each_iqr(generated_data: pd.DataFrame):
    quartiles = (
        generated_data.groupby("mine")["output"]
        .quantile([0.25, 0.75])
        .unstack()
    )
    iqr = quartiles[0.75] - quartiles[0.25]
    return iqr


def calculate_total_iqr(daily_total: pd.DataFrame):
    quartiles = daily_total["output"].quantile([0.25, 0.75])
    iqr = quartiles[0.75] - quartiles[0.25]
    return iqr
