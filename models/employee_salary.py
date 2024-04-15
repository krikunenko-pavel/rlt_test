from enum import StrEnum
from pydantic import BaseModel
from datetime import datetime


class AggregateBy(StrEnum):
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"


class RequestModel(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: AggregateBy


class ResponseModel(BaseModel):
    dataset: list[int]
    labels: list[str]
