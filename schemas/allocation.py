from dataclasses import Field
from typing import List

from pydantic import BaseModel

from schemas.task import TaskResponse


class AllocationResult(BaseModel):
    allocated_tasks: List[TaskResponse]
    total_effort_used: int
    total_effort_available: int
