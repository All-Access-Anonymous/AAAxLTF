from pydantic import BaseModel, ValidationError, validator
from typing import List


class AttendeeConfig(BaseModel):
    lateness: tuple[float, float] = (0.5, 0.9)


class SimConfig(BaseModel):
    days: int = 50
    attendee_count: int = 50
    attendee_config: AttendeeConfig = AttendeeConfig()

    seating_levels: int = 5

    @validator('days', always=True)
    def check_day_input(cls, v):
        assert isinstance(v, int) and v >= 1
        return v

    @validator('attendee_count', always=True)
    def check_attendee_count_input(cls, v):
        assert isinstance(v, int) and v >= 50
        return v

    @validator('seating_levels', always=True)
    def check_seating_levels_input(cls, v):
        assert isinstance(v, int) and v >= 0
        return v