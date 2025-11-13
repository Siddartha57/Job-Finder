from datetime import date, datetime
from pydantic import BaseModel

class JobBase(BaseModel):
    id: int
    external_id: str | None
    title: str
    company: str | None
    location: str | None
    description: str | None
    registration_close_date: date | None
    source_link: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
