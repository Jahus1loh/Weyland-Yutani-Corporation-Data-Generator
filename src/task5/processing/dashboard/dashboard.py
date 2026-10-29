import pandas as pd
import streamlit as st
from processing.dashboard.dashboard_charts import render_charts
from processing.data_analysis.helper_funcs import (
    get_max_distance,
    identify_distance_outliers,
)


def render_threshold_slider(generated_data, value_col, title):
    max_distance = get_max_distance(generated_data, value_col)
    slider_max = max(max_distance, 1.0)
    return st.slider(
        "Distance from average threshold",
        0.0,
        slider_max,
        min(max_distance / 2, slider_max),
        step=slider_max / 100,
        key=f"distance_threshold_{title}",
    )


def render_metrics(generated_data, value_col, outliers):
    stats = generated_data[value_col].agg(["mean", "median", "std"])
    values = [
        ("Mean", stats["mean"]),
        ("Median", stats["median"]),
        ("Std. deviation", stats["std"]),
        ("Distance outliers", len(outliers)),
    ]
    for column, (label, value) in zip(st.columns(4), values):
        column.metric(
            label,
            f"{value:,.2f}" if label != "Distance outliers" else str(value),
        )


def render_outlier_table(outliers):
    with st.expander(f"Distance outliers ({len(outliers)})"):
        st.dataframe(outliers, use_container_width=True)


def render_anomaly_tables(method_outliers: dict[str, pd.DataFrame]):
    with st.expander("Compare detection methods"):
        for method, outliers in method_outliers.items():
            st.write(f"{method}: {len(outliers)} observations")
            st.dataframe(outliers, use_container_width=True)


def render_dashboard(
    generated_data: pd.DataFrame,
    value_col: str,
    title: str,
    method_outliers: dict[str, pd.DataFrame] | None = None,
):
    st.header(title)
    if generated_data.empty:
        st.info("No production generated_data available.")
        return
    threshold = render_threshold_slider(generated_data, value_col, title)
    outliers = identify_distance_outliers(generated_data, value_col, threshold)
    render_metrics(generated_data, value_col, outliers)
    render_charts(generated_data, value_col, outliers)
    render_outlier_table(outliers)
    if method_outliers:
        render_anomaly_tables(method_outliers)
