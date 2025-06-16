import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Konfiguracja bazy danych
    DATABASE_CONFIG = {
        "host": os.environ.get("DB_HOST") or "localhost",
        "port": int(os.environ.get("DB_PORT") or 3306),
        "user": os.environ.get("DB_USER") or "plan",
        "password": os.environ.get("DB_PASSWORD") or "lekcji",
        "database": os.environ.get("DB_NAME") or "plan_lekcji",
        "raise_on_warnings": True,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    }

    # Ustawienia Flask
    DEBUG = os.environ.get("FLASK_DEBUG") or True
    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    DEBUG = False

    # W produkcji użyj zmiennych środowiskowych
    DATABASE_CONFIG = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", 3306)),
        "user": os.environ.get("DB_USER", "plan"),
        "password": os.environ.get("DB_PASSWORD", "lekcji"),
        "database": os.environ.get("DB_NAME", "plan_lekcji"),
        "raise_on_warnings": True,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    }


# Wybór konfiguracji na podstawie zmiennej środowiskowej
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
