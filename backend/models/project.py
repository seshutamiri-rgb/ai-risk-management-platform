
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"


class Project(BaseModel):
    project_id: str
    project_name: str = Field(min_length=3)
    project_manager: str
    start_date: date
    planned_end_date: date
    budget: float = Field(gt=0)
    status: ProjectStatus = ProjectStatus.PLANNING