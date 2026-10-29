import datetime
from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd
from structures.data_types import DatesRangeType, EventType, GeneratorDataType


def generate_data(extracted_data: GeneratorDataType) -> pd.DataFrame:
    dates = generate_dates(extracted_data["dates_range"])
    events = prepare_events(extracted_data["events"])
    records = generate_records(extracted_data, dates, events)
    return pd.DataFrame(records)


def generate_dates(dates_range: DatesRangeType):
    start_date = dates_range["start_date"]
    days_count = dates_range["days_count"]
    return [
        start_date + datetime.timedelta(days=day) for day in range(days_count)
    ]


def generate_records(
    extracted_data: GeneratorDataType,
    dates: Sequence[datetime.date],
    events: Sequence[EventType],
) -> Sequence[Mapping[str, str]]:
    records = []
    for mine in extracted_data["mines"]:
        values = generate_base_output(len(dates), extracted_data["random"])
        records.extend(
            create_mine_records(mine, dates, values, extracted_data, events)
        )
    return records


def create_mine_records(
    mine: str,
    dates: Sequence[datetime.date],
    values: np.array,
    extracted_data: Mapping[str, str],
    events: Sequence[Mapping[str, str]],
) -> Sequence[Mapping[str, str]]:
    return [
        create_record(mine, date, values[day], day, extracted_data, events)
        for day, date in enumerate(dates)
    ]


def create_record(
    mine: str,
    date: datetime.date,
    base_output: float,
    day: int,
    extracted_data: Mapping[str, str],
    events: Sequence[Mapping[str, str]],
) -> Mapping[str, str]:
    output = calculate_output(base_output, date, day, extracted_data, events)
    return {"date": date, "mine": mine, "output": round(output, 2)}


def calculate_output(
    base_output: float,
    date: datetime.date,
    day: int,
    extracted_data: Mapping[str, str],
    events: Sequence[Mapping[str, str]],
) -> float:
    weekday = extracted_data["daily_output"][date.strftime("%A")]
    growth = (1 + extracted_data["daily_growth"]) ** day
    event_factor = get_event_factor(date, events)
    return max(0.0, base_output * weekday * growth * event_factor)


def generate_base_output(
    days_count: int,
    random_config: dict,
) -> np.ndarray:
    distribution = random_config["distribution"]
    if distribution == "normal":
        return generate_normal_output(days_count, random_config)
    return generate_uniform_output(days_count, random_config)


def generate_normal_output(
    days_count: int,
    extracted_data: dict,
) -> np.ndarray:
    mean, deviation = extracted_data["mean"], extracted_data["deviation"]
    correlation = extracted_data["correlation"]
    output = np.empty(days_count)
    output[0] = np.random.normal(mean, deviation)
    innovation = deviation * np.sqrt(1 - correlation**2)
    for day in range(1, days_count):
        output[day] = (
            mean
            + correlation * (output[day - 1] - mean)
            + np.random.normal(0, innovation)
        )
    return output


def generate_uniform_output(
    days_count: int,
    extracted_data: dict,
) -> np.ndarray:
    return np.random.uniform(
        extracted_data["min"],
        extracted_data["max"],
        size=days_count,
    )


def prepare_events(
    events: Sequence[Mapping[str, str]],
):
    return [event for event in events if np.random.random() < event["probability"]]


def get_event_factor(date: datetime.date, events: Sequence[Mapping[str, str]]):
    factor = 1
    for event in events:
        if is_event_active(date, event):
            factor *= event["factor"]
    return factor


def is_event_active(date: datetime.date, event: dict) -> bool:
    event_end = event["start_date"] + datetime.timedelta(days=event["duration"])
    return event["start_date"] <= date < event_end
