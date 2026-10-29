import pandas as pd


def calculate_mean_std_median(generated_data: pd.DataFrame):
    each_mine_stats = calculate_each_mean_std_median(generated_data)
    total_mines_stats = calculate_total_mean_std_median(generated_data)
    return {
        "each_mine_stats": each_mine_stats,
        "total_stats": total_mines_stats,
    }


def calculate_each_mean_std_median(generated_data: pd.DataFrame):
    each_mine_stats = generated_data.groupby("mine")["output"].agg(
        ["mean", "std", "median"]
    )
    return each_mine_stats


def calculate_total_mean_std_median(generated_data: pd.DataFrame):
    daily_total = generated_data.groupby("date")["output"].sum()
    total_mines_stats = daily_total.agg(["mean", "std", "median"])
    return total_mines_stats