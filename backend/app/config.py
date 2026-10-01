
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "AI Risk Management Platform"

    # Snowflake connection settings
    snowflake_account: str = ""
    snowflake_user: str = ""
    snowflake_password: SecretStr = SecretStr("")
    snowflake_database: str = "AI_RISK_DB"
    snowflake_schema: str = "PROJECT_DATA"
    snowflake_warehouse: str = ""
    snowflake_role: str = ""

    
    # LLM provider settings
    llm_provider: str = "openrouter"
    llm_api_key: SecretStr = SecretStr("")
    llm_model: str = "openai/gpt-4o-mini"
    llm_base_url: str = "https://openrouter.ai/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()