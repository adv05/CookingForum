import os
import secrets


# App variables
API_STRING: str = os.environ.get("API_STRING", "/api/v1")
PROJECT_NAME: str = "CookingForum"
DEBUG_MODE: str = os.environ.get("DEBUG_MODE", "False")
VERBOSITY: str = os.environ.get("VERBOSITY", "DEBUG")
ADMIN_PASSWORD: str = os.environ.get("BE_ADMIN_PASSWORD")

# Database configuration
DB_CONFIG = {
    "db_name": os.getenv("DB_NAME", "postgres"),
    "db_user": os.getenv("DB_USER", "postgres"),
    "db_password": os.getenv("DB_PASSWORD", "example"),
    "db_port": os.getenv("DB_PORT", "5432"),
    "db_host": os.getenv("DB_HOST", "0.0.0.0"),
}

# Application Path
APP_PATH: str = os.environ.get("PROJECT_WORKSPACE", os.path.abspath("."))

# Applications configurations
# Read the application configuration settings
config_path: str = os.path.join(APP_PATH, "app", "config")

SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.environ.get("SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES", 48 * 60)
)

ENCODING_ALGORITHM: str = os.environ.get("ENCODING_ALGORITHM", "HS256")
ENCODE_TOKEN_KEY: str = os.environ.get(
    "ENCODE_TOKEN_KEY", secrets.token_urlsafe(32)
)
