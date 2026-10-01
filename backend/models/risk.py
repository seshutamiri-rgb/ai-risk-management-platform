
from enum import Enum

from pydantic import BaseModel, Field


class RiskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    MITIGATED = "mitigated"
    CLOSED = "closed"


class Risk(BaseModel):
    risk_id: str
    project_id: str
    title: str = Field(min_length=3)
    description: str
    probability: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    owner: str
    mitigation_plan: str
    status: RiskStatus = RiskStatus.OPEN