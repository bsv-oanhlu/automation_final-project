import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)

BASE_URL = os.getenv(
    "BASE_URL",
    "https://bsv-nhungnguyen.github.io/bai_tap_17082026.html",
).strip()

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
GUEST_USER = os.getenv("GUEST_USER", "guest")
GUEST_PASSWORD = os.getenv("GUEST_PASSWORD", "guest123")
