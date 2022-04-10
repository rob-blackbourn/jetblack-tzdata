"""Types"""

from datetime import datetime, timedelta
from typing import TypedDict


class TimezoneDelta(TypedDict):
    utc: datetime
    local: datetime
    offset: timedelta
    abbr: str
    isDst: bool


class MinTimezoneDelta(TypedDict):
    u: int
    o: int
    a: str
    d: int
