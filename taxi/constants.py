import re


LICENSE_PATTERN = r"^[A-Z]{3}\d{5}$"
LICENSE_RE = re.compile(LICENSE_PATTERN)
LICENSE_MESSAGE = (
    "License must be 8 chars: 3 uppercase letters + 5 digits (e.g. ABC12345)."
)
