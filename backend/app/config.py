import os


class Settings:
    FIREBIRD_DSN: str = os.getenv("FIREBIRD_DSN", "localhost:/firebird/data/shelter.fdb")
    FIREBIRD_USER: str = os.getenv("FIREBIRD_USER", "SYSDBA")
    FIREBIRD_PASSWORD: str = os.getenv("FIREBIRD_PASSWORD", "masterkey")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production-please")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    ASANA_TOKEN: str = os.getenv("ASANA_TOKEN", "")
    ASANA_PROJECT_GID: str = os.getenv("ASANA_PROJECT_GID", "")
    JIRA_URL: str = os.getenv("JIRA_URL", "")
    JIRA_USER_EMAIL: str = os.getenv("JIRA_USER_EMAIL", "")
    JIRA_API_TOKEN: str = os.getenv("JIRA_API_TOKEN", "")
    JIRA_PROJECT_KEY: str = os.getenv("JIRA_PROJECT_KEY", "")


settings = Settings()
