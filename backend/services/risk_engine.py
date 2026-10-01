
def calculate_risk_score(probability: int, impact: int) -> int:
    """Calculate a risk score using probability multiplied by impact."""
    if not 1 <= probability <= 5:
        raise ValueError("Probability must be between 1 and 5.")

    if not 1 <= impact <= 5:
        raise ValueError("Impact must be between 1 and 5.")

    return probability * impact


def classify_risk(score: int) -> str:
    """Classify a risk score using the project's configured bands."""
    if not 1 <= score <= 25:
        raise ValueError("Risk score must be between 1 and 25.")

    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 16:
        return "High"
    return "Critical"


def assess_risk(probability: int, impact: int) -> dict:
    """Return the calculated score and risk classification."""
    score = calculate_risk_score(probability, impact)

    return {
        "probability": probability,
        "impact": impact,
        "risk_score": score,
        "risk_level": classify_risk(score),
    }