import datetime
import math
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path

with Path("src/task5/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    weekdays = cfg["general"]["weekdays"]


def validate_days_count(days_count: str) -> None:
    check_if_days_count_can_be_integer(days_count)
    check_days_count_larger_than_0(days_count)


def validate_start_date(start_date: str) -> None:
    check_correct_datetime_format(start_date)


def validate_mines(mines: Sequence[str]) -> None:
    check_mines_not_empty(mines)
    check_mine_names_valid(mines)
    check_mine_names_unique(mines)


def validate_uniform_distr(minimum: str, maximum: str) -> None:
    low = check_finite_number(minimum, "Minimum")
    high = check_finite_number(maximum, "Maximum")

    if low >= high:
        raise ValueError("Minimum must be smaller than maximum")


def validate_normal_distr(mean: str, deviation: str, correlation: str) -> None:
    check_finite_number(mean, "Mean")
    check_deviation_positive(deviation)
    check_correlation_range(correlation)


def validate_daily_output(daily_output: Mapping[str, str]) -> None:
    for weekday in weekdays:
        if weekday not in daily_output:
            raise ValueError(f"Missing weekday factor: {weekday}")
        num = daily_output[weekday].replace(",", "")
        factor = check_finite_number(num, f"{weekday} factor")
        if factor < 0:
            raise ValueError(f"{weekday} factor cannot be negative")


def validate_daily_growth(daily_growth: str) -> None:
    growth = check_percentage(daily_growth, "Daily growth")

    if growth <= -1:
        raise ValueError("Daily growth must be greater than -100%")


def validate_events(events: Sequence[Mapping[str, str]]) -> None:
    for index, event in enumerate(events):
        try:
            validate_event(event)
        except (KeyError, ValueError) as error:
            raise ValueError(
                f"Invalid event at row {index + 1}: {error}"
            ) from error


def validate_event(event: Mapping[str, str]) -> None:
    check_correct_datetime_format(event["start_date"])

    duration = check_finite_number(event["duration"].replace(",", ""), "Event duration")
    factor = check_finite_number(event["factor"].replace(",", ""), "Event factor")
    probability = check_probability(event["probability"].replace(",", ""))

    if not duration.is_integer() or duration < 1:
        raise ValueError("Event duration must be a positive integer")

    if factor < 0:
        raise ValueError("Event factor cannot be negative")

    if not 0 <= probability <= 1:
        raise ValueError("Event probability must be between 0 and 1")


def check_if_days_count_can_be_integer(days_count: str) -> None:
    try:
        int(days_count)
    except ValueError:
        raise ValueError("Days count must be an integer")


def check_days_count_larger_than_0(days_count: str) -> None:
    if int(days_count) <= 0:
        raise ValueError("Days count must be larger than 0")


def check_correct_datetime_format(start_date: str) -> None:
    try:
        datetime.date.fromisoformat(start_date)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def check_mines_not_empty(mines: Sequence[str]) -> None:
    if isinstance(mines, (str, bytes)) or not mines:
        raise ValueError("At least one mine is required")


def check_mine_names_valid(mines: Sequence[str]) -> None:
    if any(not isinstance(mine, str) or not mine.strip() for mine in mines):
        raise ValueError("Mine names must be non-empty strings")


def check_mine_names_unique(mines: Sequence[str]) -> None:
    normalized = [mine.strip().casefold() for mine in mines]
    if len(normalized) != len(set(normalized)):
        raise ValueError("Mine names must be unique")


def check_deviation_positive(deviation: str) -> None:
    if check_finite_number(deviation, "Deviation") <= 0:
        raise ValueError("Deviation must be larger than 0")


def check_correlation_range(correlation: str) -> None:
    value = check_finite_number(correlation, "Correlation")
    if not -0.99 <= value <= 0.99:
        raise ValueError("Correlation must be between -0.99 and 0.99")


def check_percentage(value: str, name: str) -> float:
    text = str(value).strip()
    if not text.endswith("%"):
        raise ValueError(f"{name} must end with '%'")

    return check_finite_number(text[:-1].strip(), name) / 100


def check_probability(probability: str) -> float:
    value = check_finite_number(probability, "Probability")
    if not 0 <= value <= 1:
        raise ValueError("Probability must be between 0 and 1")
    return value


def check_finite_number(value: object, name: str) -> float:
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{name} must be a number") from None

    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number")

    return number
