from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    date: datetime
    start_prompt: str
    report: Optional[str]


class ReportUpdate(ReportBase):
    date: Optional[datetime]
    start_prompt: Optional[str]


class ReportCreate(ReportBase):
    pass


class ReportDB(ReportBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_date: datetime
    update_date: datetime
