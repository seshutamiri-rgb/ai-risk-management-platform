
import snowflake.connector
from backend.services.risk_engine import assess_risk

from backend.app.config import settings



def get_snowflake_connection():
    """Create a connection using local environment settings."""
    required = {
        "SNOWFLAKE_ACCOUNT": settings.snowflake_account,
        "SNOWFLAKE_USER": settings.snowflake_user,
        "SNOWFLAKE_PASSWORD": (
            settings.snowflake_password.get_secret_value()
        ),
        "SNOWFLAKE_DATABASE": settings.snowflake_database,
        "SNOWFLAKE_SCHEMA": settings.snowflake_schema,
        "SNOWFLAKE_WAREHOUSE": settings.snowflake_warehouse,
        "SNOWFLAKE_ROLE": settings.snowflake_role,
    }

    missing = [
        name for name, value in required.items()
        if not value or not value.strip()
    ]

    if missing:
        raise ValueError(
            "Missing Snowflake settings: " + ", ".join(missing)
        )

    return snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=(
            settings.snowflake_password.get_secret_value()
        ),
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
        role=settings.snowflake_role,
        login_timeout=20,
        network_timeout=30,
    )


def _fetch_all(query: str) -> list[dict]:
    """Execute an internal read-only query and return dictionaries."""
    connection = None
    cursor = None

    try:
        connection = get_snowflake_connection()
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [
            column[0].lower()
            for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def fetch_projects() -> list[dict]:
    """Retrieve project records from Snowflake."""
    query = """
        SELECT
            PROJECT_ID,
            PROJECT_NAME,
            PROJECT_MANAGER,
            START_DATE,
            PLANNED_END_DATE,
            BUDGET,
            STATUS
        FROM AI_RISK_DB.PROJECT_DATA.PROJECTS
        ORDER BY PROJECT_ID
    """

    return _fetch_all(query)


def fetch_risks() -> list[dict]:
    """Retrieve risk records and calculate their score and severity."""

    query = """
        SELECT
            RISK_ID,
            PROJECT_ID,
            TITLE,
            DESCRIPTION,
            PROBABILITY,
            IMPACT,
            OWNER,
            MITIGATION_PLAN,
            STATUS
        FROM AI_RISK_DB.PROJECT_DATA.RISKS
        ORDER BY RISK_ID
    """

    risks = _fetch_all(query)
    enriched_risks = []

    for risk in risks:
        probability = int(risk["probability"])
        impact = int(risk["impact"])

        assessment = assess_risk(
            probability=probability,
            impact=impact,
        )

        enriched_risks.append({
            **risk,
            "risk_score": assessment["risk_score"],
            "risk_level": assessment["risk_level"],
        })

    return enriched_risks


def fetch_project_risk_summary(project_id: str) -> dict:
    """Build a risk summary for one project using Snowflake data."""
    from backend.services.risk_engine import assess_risk

    all_risks = fetch_risks()

    project_risks = [
        risk
        for risk in all_risks
        if risk["project_id"] == project_id
    ]

    summary = {
        "project_id": project_id,
        "total_risks": len(project_risks),
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0,
    }

    for risk in project_risks:
        assessment = assess_risk(
            probability=int(risk["probability"]),
            impact=int(risk["impact"]),
        )

        level = str(assessment["risk_level"]).lower()

        if level in summary:
            summary[level] += 1

    return summary
    