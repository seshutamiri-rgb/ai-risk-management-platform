
import sys
from pathlib import Path

# Make the project root available to Python imports.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.snowflake_service import (
    fetch_projects,
    fetch_risks,
)


def main():
    try:
        projects = fetch_projects()
        risks = fetch_risks()

        print("Snowflake data retrieval: SUCCESS")
        print(f"Projects retrieved: {len(projects)}")

        for project in projects:
            print(
                f"  {project['project_id']}: "
                f"{project['project_name']}"
            )

        print(f"Risks retrieved: {len(risks)}")

        for risk in risks:
            score = int(risk["probability"]) * int(risk["impact"])
            print(
                f"  {risk['risk_id']}: "
                f"score={score}, "
                f"project={risk['project_id']}"
            )

        if len(projects) != 2 or len(risks) != 3:
            print("Verification failed: unexpected record counts.")
            raise SystemExit(1)

        print("Record count verification: PASSED")

    except SystemExit:
        raise
    except Exception as exc:
        # Avoid printing raw exception messages or credentials.
        print("Snowflake data retrieval: FAILED")
        print("Error type:", type(exc).__name__)
        raise SystemExit(1)


if __name__ == "__main__":
    main()