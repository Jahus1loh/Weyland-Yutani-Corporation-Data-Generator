import pandas as pd
import streamlit as st
from processing.dashboard.dashboard_charts import render_charts
from processing.data_analysis.analyze_data import analyze_data
from processing.data_analysis.helper_funcs import (
    get_max_distance,
    identify_distance_outliers,
)
from processing.report.pdf_generator import generate_pdf_report

st.set_page_config(
    page_title="Weyland-Yutani Mine Analytics",
    layout="wide",
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
        st.dataframe(outliers, width="stretch")


def render_anomaly_tables(method_outliers: dict[str, pd.DataFrame]):
    with st.expander("Compare detection methods"):
        for method, outliers in method_outliers.items():
            st.write(f"{method}: {len(outliers)} observations")
            st.dataframe(outliers, width="stretch")


def render_outlier_summary(results):
    summary = pd.DataFrame(
        [
            {"Method": name, "Flagged observations": len(rows)}
            for name, rows in results.items()
        ]
    )
    st.dataframe(summary, hide_index=True, width="stretch")


def render_outlier_tables(results):
    for name, rows in results.items():
        with st.expander(f"{name} ({len(rows)} flagged)"):
            if rows.empty:
                st.caption("No observations flagged by this method")
            else:
                st.dataframe(rows, hide_index=True, width="stretch")


def render_pdf_controls(data, title, threshold, results):
    key = f"pdf_report_{title}"
    if st.button("Generate PDF report", key=f"generate_{title}"):
        st.session_state[key] = generate_pdf_report(
            data, title, threshold, results
        )
    if key in st.session_state:
        st.download_button(
            "Download PDF",
            data=st.session_state[key],
            file_name=f"{title.lower().replace(' ', '_')}_report.pdf",
            mime="application/pdf",
            key=f"download_{title}",
        )


def render_dashboard(
    generated_data: pd.DataFrame,
    value_col: str,
    title: str,
    method_outliers: dict[str, pd.DataFrame] | None = None,
):
    st.header(title)
    if generated_data.empty:
        st.info("No production generated_data available")
        return
    threshold = render_threshold_slider(generated_data, value_col, title)
    outliers = identify_distance_outliers(generated_data, value_col, threshold)
    render_metrics(generated_data, value_col, outliers)
    render_charts(generated_data, value_col, outliers)
    render_outlier_table(outliers)
    if method_outliers:
        render_anomaly_tables(method_outliers)
    render_pdf_controls(generated_data, title, threshold, outliers)
