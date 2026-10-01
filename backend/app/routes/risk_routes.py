
from fastapi import APIRouter, Query

from backend.services.risk_engine import assess_risk

router = APIRouter(
    prefix="/risks",
    tags=["Risk Management"],
)


@router.get("/assess")
def assess_project_risk(
    probability: int = Query(ge=1, le=5),
    impact: int = Query(ge=1, le=5),
):
    return assess_risk(probability, impact)