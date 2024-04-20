import os

config = {
    "POSTGRES_DB": os.environ.get("POSTGRES_DB", "postgres"),
    "POSTGRES_USER": os.environ.get("POSTGRES_USER", "postgres"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
    "POSTGRES_HOST": os.environ.get("POSTGRES_HOST", "db"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT", 5432),
}