import datetime
from collections.abc import Mapping, Sequence

from processing.data_generator.validate_extracted_aspects import (
    validate_daily_growth,
    validate_daily_output,
    validate_days_count,
    validate_events,
    validate_mines,
    validate_normal_distr,
    validate_start_date,
    validate_uniform_distr,
)


def clean_days_count(days_count: str) -> int:
    validate_days_count(days_count)
    return int(days_count)


def clean_start_date(start_date: str) -> datetime.date:
    validate_start_date(start_date)
    return datetime.date.fromisoformat(start_date)


def clean_mines(mines: Sequence[str]) -> list[str]:
    validate_mines(mines)
    return [mine.strip() for mine in mines]


def clean_normal_distr(
    mean: str,
    deviation: str,
    correlation: str,
) -> Mapping[str, float]:
    validate_normal_distr(mean, deviation, correlation)
    return {
        "mean": float(mean),
        "deviation": float(deviation),
        "correlation": float(correlation),
    }


def clean_uniform_distr(
    minimum: str,
    maximum: str,
) -> Mapping[str, float]:
    validate_uniform_distr(minimum, maximum)
    return {"min": float(minimum), "max": float(maximum)}


def clean_daily_output(daily_output: Mapping) -> Mapping[str, float]:
    validate_daily_output(daily_output)
    return {weekday: float(factor) for weekday, factor in daily_output.items()}


def clean_daily_growth(daily_growth: str) -> Mapping[str, float]:
    validate_daily_growth(daily_growth)
    value = daily_growth.strip().removesuffix("%")
    return {"daily_growth": float(value) / 100}


def clean_events(events: Sequence[Mapping]) -> list[Mapping]:
    validate_events(events)
    cleaned_events = []
    for event in events:
        cleaned_events.append(
            {
                "start_date": datetime.date.fromisoformat(event["start_date"]),
                "duration": int(float(event["duration"])),
                "factor": float(event["factor"]),
                "probability": float(event["probability"]),
            }
        )
    return cleaned_events
