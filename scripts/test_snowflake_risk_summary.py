
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.snowflake_service import (
    fetch_project_risk_summary,
)


def main():
    for project_id in ["PRJ-001", "PRJ-002"]:
        summary = fetch_project_risk_summary(project_id)

        print(f"\nProject: {project_id}")
        print(summary)


if __name__ == "__main__":
    main()