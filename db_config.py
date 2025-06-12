# Konfiguracja bazy danych dla Flask
import os

# Import konfiguracji Flask jeśli dostępna
try:
    from config import Config
    config = Config.DATABASE_CONFIG
except ImportError:
    # Fallback configuration
    config = {
        "host": os.environ.get('DB_HOST', "localhost"),
        "port": int(os.environ.get('DB_PORT', 3306)),
        "user": os.environ.get('DB_USER', "root"),
        "password": os.environ.get('DB_PASSWORD', ""),
        "database": os.environ.get('DB_NAME', "plan_lekcji"),
        "raise_on_warnings": True,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci"
    }