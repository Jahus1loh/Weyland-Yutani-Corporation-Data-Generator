import datetime

from collections.abc import Sequence, Mapping
from typing import TypedDict


class EventType[TypedDict]:
    start_date: datetime.date
    duration: int
    factor: float
    probability: float


class DatesRangeType[TypedDict]:
    start_date: datetime.date
    days_count: int


class MinesType[TypedDict]:
    mines: Sequence[str]


class RandomType[TypedDict]:
    distribution: str
    mean: float
    deviation: float
    correlation: float
    min: float
    max: float


class GeneratorDataType[TypedDict]:
    dates_range: DatesRangeType
    mines: MinesType
    random: RandomType
    daily_output: Mapping[str, float]
    daily_growth: float
    events: EventType