# app/schemas/task.py
from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    effort: int
    date_added: date
    time_added: time


class TaskResponse(TaskBase):
    task_id: int
    user_name: str
    team_name: str
    priority_name: str
    priority_value: int
    description: str

    class Config:
        from_attributes = True


class TaskFilter(BaseModel):
    team: Optional[str] = None
