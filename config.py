import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)


def _require(name: str) -> str:
    """Read a required value from .env — credentials are never hardcoded in the repo."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing '{name}'. Copy .env.example to .env and fill in the value "
            f"(see README → Environment)."
        )
    return value


BASE_URL = _require("BASE_URL")

ADMIN_USER = _require("ADMIN_USER")
ADMIN_PASSWORD = _require("ADMIN_PASSWORD")
GUEST_USER = _require("GUEST_USER")
GUEST_PASSWORD = _require("GUEST_PASSWORD")
