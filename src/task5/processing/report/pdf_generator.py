import tomllib
from html import escape
from io import BytesIO
from pathlib import Path

import pandas as pd
from processing.dashboard.dashboard_charts import (
    create_box_figure,
    create_histogram,
    create_production_figure,
    create_weekday_figure,
)
from processing.data_analysis.helper_funcs import (
    to_frame,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

with Path("src/task5/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    value_column = cfg["pdf"]["value_column"]
    date_column = cfg["pdf"]["date_column"]
    company_name = cfg["pdf"]["company_name"]

    page_margin = cfg["pdf"]["page_margin"] * cm
    small_gap = cfg["pdf"]["small_gap"] * cm
    large_gap = cfg["pdf"]["large_gap"] * cm

    charts_per_page = cfg["pdf"]["charts_per_page"]

chart_px = {"width": 1200, "height": 520, "scale": 1}
chart_size = {"width": 17 * cm, "height": 7.4 * cm}


def _fmt_count(value) -> str:
    return f"{value:,}"


def _fmt_number(value) -> str:
    return f"{value:,.2f}"


def _chunked(items, size):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def create_summary_rows(data, threshold):
    stats = data[value_column].agg(["mean", "median", "std", "min", "max"])
    return [
        ["Metric", "Value"],
        ["Days analyzed", _fmt_count(len(data))],
        ["Mean output", _fmt_number(stats["mean"])],
        ["Median output", _fmt_number(stats["median"])],
        ["Standard deviation", _fmt_number(stats["std"])],
        ["Minimum output", _fmt_number(stats["min"])],
        ["Maximum output", _fmt_number(stats["max"])],
        ["Distance threshold", _fmt_number(threshold)],
    ]


def create_outlier_summary_rows(results):
    return [["Detection method", "Flagged observations"]] + [
        [method, _fmt_count(len(rows))] for method, rows in results.items()
    ]


def create_outlier_records(rows):
    return [["Date", "Output"]] + [
        [str(date), f"{value:,.2f}"]
        for date, value in zip(rows["date"], rows["output"])
    ]


def create_report_table(rows):
    rows = [list(row) for row in rows]
    if not rows:
        rows = [["No data available"]]
    table = Table(rows, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#273244")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def create_chart_image(figure):
    png = figure.to_image(format="png", **chart_px)
    return Image(BytesIO(png), **chart_size)


def create_report_figures(data, outliers):
    return [
        create_production_figure(data, value_column, outliers),
        create_box_figure(data, value_column),
        create_weekday_figure(data, value_column),
        create_histogram(data, value_column),
    ]


def build_header_section(data, title, styles):
    period = f"{data[date_column].min()} to {data[date_column].max()}"
    return [
        Paragraph(company_name, styles["Title"]),
        Paragraph(
            f"Extraction Analytics - {escape(title)}", styles["Heading1"]
        ),
        Paragraph(f"Reporting period: {period}", styles["BodyText"]),
        Spacer(1, large_gap),
    ]


def build_summary_section(data, threshold, results):
    return [
        create_report_table(create_summary_rows(data, threshold)),
        Spacer(1, large_gap),
        create_report_table(create_outlier_summary_rows(results)),
    ]


def build_charts_section(data, outliers):
    figures = create_report_figures(data, outliers)
    story = []
    for page_number, page_figures in enumerate(
        _chunked(figures, charts_per_page)
    ):
        if page_number:
            story.append(PageBreak())
        for figure in page_figures:
            story += [create_chart_image(figure), Spacer(1, small_gap)]
    return story


def build_outlier_section(results, styles):
    story = [Paragraph("Flagged observations", styles["Heading1"])]
    for method, rows in results.items():
        story.append(Paragraph(escape(method), styles["Heading2"]))
        if rows.empty:
            story.append(
                Paragraph("No observations flagged.", styles["BodyText"])
            )
        else:
            story.append(create_report_table(create_outlier_records(rows)))
        story.append(Spacer(1, small_gap))
    return story


def build_story(data, title, threshold, outliers, styles):
    by_method = {name: to_frame(o, data) for name, o in outliers.items()}
    return [
        *build_header_section(data, title, styles),
        *build_summary_section(data, threshold, outliers),
        PageBreak(),
        *build_charts_section(data, outliers),
        PageBreak(),
        *build_outlier_section(by_method, styles),
    ]


def render_pdf(story) -> bytes:
    buffer = BytesIO()
    SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=page_margin,
        leftMargin=page_margin,
        topMargin=page_margin,
        bottomMargin=page_margin,
    ).build(story)
    return buffer.getvalue()


def generate_pdf_report(data, title, threshold, outliers):
    styles = getSampleStyleSheet()
    story = build_story(data, title, threshold, outliers, styles)
    return render_pdf(story)
