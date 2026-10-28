import datetime
from pathlib import Path
import tomllib
from collections.abc import Sequence

from processing.data_generator.clean_extracted_aspects import (
    clean_daily_growth,
    clean_daily_output,
    clean_days_count,
    clean_events,
    clean_mines,
    clean_normal_distr,
    clean_start_date,
    clean_uniform_distr,
)

with Path("src/task5/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    weekdays = cfg["general"]["weekdays"]


def extract_mines_aspects(spreadsheet_data):
    events = []
    for i, row in enumerate(spreadsheet_data):
        if i == 2:
            start_date_row = process_start_date_row(row)
        if i == 3:
            mines_row = process_mines_row(row)
        if i == 5:
            distr_row = process_distribution_row(row)
        if i == 6:
            daily_output = process_daily_output_row(row)
        if i == 7:
            daily_growth = process_daily_growth_row(row)
        if i > 8:
            events.append(process_event_row(row))

    return {
        "dates_range": start_date_row,
        "mines": mines_row,
        "random": distr_row,
        "daily_output": daily_output,
        "daily_growth": daily_growth,
        "events": clean_events(events),
    }


def process_start_date_row(row: Sequence[str]) -> dict[str, str]:
    start_date = retrieve_start_date(row)
    days_count = retrieve_days_count(row)
    return {"start_date": start_date, "days_count": days_count}


def process_mines_row(row: Sequence[str]) -> Sequence[str]:
    rows_with_mines = row[1:]
    last_mine_index = rows_with_mines.index("")
    rows_with_mines = rows_with_mines[:last_mine_index]
    return clean_mines(rows_with_mines)


def process_distribution_row(row: Sequence[str]) -> dict[str, object]:
    if row[1] == "Normal":
        random_aspects = process_normal_distribution(row[2:5])
    else:
        random_aspects = process_uniform_distribution(row[2:4])
    return random_aspects


def process_normal_distribution(
    normal_distr_row: Sequence[str],
) -> dict[str, float]:
    mean_data = normal_distr_row[0]
    deviation_data = normal_distr_row[1]
    correlation_data = normal_distr_row[2]
    return clean_normal_distr(
        mean_data, deviation_data, correlation_data
    )


def process_uniform_distribution(
    uniform_distr_row: Sequence[str],
) -> dict[str, str]:
    min_data = uniform_distr_row[0]
    max_data = uniform_distr_row[1]
    return clean_uniform_distr(
        min_data, max_data
    )


def process_daily_output_row(row: Sequence[str]) -> dict[str, str]:
    daily_output_row = {}
    for i, weekday in enumerate(weekdays):
        daily_output_row[weekday] = row[i + 1]
    return clean_daily_output(daily_output_row)


def process_daily_growth_row(row: Sequence[str]):
    daily_growth = row[1]
    return clean_daily_growth(daily_growth)


def process_event_row(row: Sequence[str]):
    event_start_date = row[1]
    event_duration = row[2]
    event_factor = row[3]
    event_probability = row[4]
    return {
        "start_date": event_start_date,
        "duration": event_duration,
        "factor": event_factor,
        "probability": event_probability,
    }


def retrieve_start_date(start_date_row: Sequence[str]) -> datetime.date:
    start_date = start_date_row[1]
    return clean_start_date(start_date)


def retrieve_days_count(start_date_row: Sequence[str]) -> int:
    days_count = start_date_row[2]
    return clean_days_count(days_count)
