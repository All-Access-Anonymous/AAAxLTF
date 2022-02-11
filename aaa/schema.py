from pydantic import BaseModel
from typing import List

class AttendeeConfig(BaseModel):
    lateness: tuple[float, float] = (0.5, 0.9)


class SimConfig(BaseModel):
    days: int = 50
    attendee_count: int = 50
    attendee_config: AttendeeConfig = AttendeeConfig()
    seating_levels: int = 5

#sc = SimConfig()
#print(sc.dict())
