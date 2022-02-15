from pydantic import BaseModel, ValidationError, validator
from typing import List


class AttendeeConfig(BaseModel):
    lateness: tuple[float, float] = (0.5, 0.9)


class SimConfig(BaseModel):
    days: int = 50
    attendee_count: int = 50
    attendee_config: AttendeeConfig = AttendeeConfig()

    seating_levels: int = -5

    @validator('days', 'attendee_count', 'seating_levels', always=True)
    def check_non_negative_vars(cls, v):
        if v <= 0:
            raise ValueError(
                'Negative or 0 value amongst days, attendee_count, or seating_levels')
