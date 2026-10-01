import sys
from pathlib import Path

import snowflake.connector

# Add the project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings


def check_snowflake_connection():
    required_settings = {
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
        name
        for name, value in required_settings.items()
        if not value or not value.strip()
    ]

    if missing:
        print("Configuration incomplete.")
        print("Missing settings:", ", ".join(missing))
        return False

    connection = None
    cursor = None

    try:
        connection = snowflake.connector.connect(
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

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA()
        """)

        role, warehouse, database, schema = cursor.fetchone()

        print("Snowflake connection: SUCCESS")
        print("Active role:", role)
        print("Active warehouse:", warehouse)
        print("Active database:", database)
        print("Active schema:", schema)

        if database != "AI_RISK_DB" or schema != "PROJECT_DATA":
            print("Warning: Database or schema differs from expected.")
            return False

        print("Database and schema verification: PASSED")
        return True

    except Exception as exc:
        # Avoid printing connection details or credentials.
        print("Snowflake connection: FAILED")
        print("Error type:", type(exc).__name__)
        print(
            "Check your account settings, authentication, "
            "network access, and Snowflake permissions."
        )
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":
    success = check_snowflake_connection()

    if not success:
        raise SystemExit(1)