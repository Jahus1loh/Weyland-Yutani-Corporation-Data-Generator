import pandas as pd
import plotly.express as px
import streamlit as st
from processing.data_analysis.chart_analysis import calculate_weekday_average
from processing.data_analysis.helper_funcs import to_frame


def style_chart(fig, title, x_title, y_title):
    fig.update_layout(
        template="plotly_white",
        title={"text": title, "x": 0.02, "xanchor": "left"},
        height=340,
        margin={"l": 20, "r": 20, "t": 60, "b": 25},
        font={"family": "Arial, sans-serif", "size": 12, "color": "#1F2937"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(title=x_title, showgrid=False, ticks="outside")
    fig.update_yaxes(title=y_title, gridcolor="#E2E8F0", zeroline=False)
    return fig


def add_outlier_markers(fig, results, data, value_col):
    for name, outliers in results.items():
        frame = to_frame(outliers, data)
        if not frame.empty:
            fig.add_scatter(
                x=frame["date"], y=frame[value_col], mode="markers",
                name=name, marker={"size": 11, "symbol": "x"},
            )
    return fig


def create_production_figure(data, value_col, outliers):
    fig = px.line(data, x="date", y=value_col, markers=True)
    fig.update_traces(line_color="#2563EB", line_width=2.5, marker_size=6)
    fig = add_outlier_markers(fig, outliers, data, value_col)
    return style_chart(fig, "Daily production", "Date", "Output (units)")


def create_box_figure(data, value_col):
    fig = px.box(data, y=value_col, points="all")
    fig.update_traces(
        marker_color="#0F766E", marker_size=5, line_color="#115E59"
    )
    return style_chart(fig, "Production distribution", "", "Output (units)")


def create_weekday_figure(data, value_col):
    averages = calculate_weekday_average(data, value_col)
    fig = px.bar(averages, x="weekday", y="average_output")
    fig.update_traces(marker_color="#0F766E", marker_line_color="white")
    return style_chart(
        fig,
        "Average by weekday",
        "Weekday",
        "Average output (units)",
    )


def create_histogram(data, value_col):
    fig = px.histogram(data, x=value_col, nbins=15)
    fig.update_traces(marker_color="#7C3AED", marker_line_color="white")
    return style_chart(
        fig, "Output frequency", "Output (units)", "Number of days"
    )


def show_chart(fig):
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def render_charts(data, value_col, outliers):
    show_chart(create_production_figure(data, value_col, outliers))
    show_chart(create_box_figure(data, value_col))
    show_chart(create_weekday_figure(data, value_col))
    show_chart(create_histogram(data, value_col))
