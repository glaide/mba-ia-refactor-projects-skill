import os
import sys

DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DB_PATH = os.environ.get("DB_PATH", "loja.db")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))
TOKEN_MAX_AGE = int(os.environ.get("TOKEN_MAX_AGE", "86400"))

_secret = os.environ.get("SECRET_KEY")
if not _secret:
    if DEBUG:
        _secret = "dev-key-change-in-production"
    else:
        print("ERROR: SECRET_KEY environment variable is required when DEBUG is false.", file=sys.stderr)
        sys.exit(1)
SECRET_KEY = _secret

DISCOUNT_TIERS = [
    (10000, 0.10),
    (5000, 0.05),
    (1000, 0.02),
]
