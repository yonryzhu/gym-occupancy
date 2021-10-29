from datetime import datetime

from pydantic import BaseModel


class Record(BaseModel):
    timestamp: datetime
    occupancy: int
    remaining: int
    ratio: float

    class Config:
        orm_mode = True
