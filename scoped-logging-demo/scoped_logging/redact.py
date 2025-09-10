# scoped-logging-demo/scoped_logging/redact.py
from __future__ import annotations
import re

SIMPLE_PATTERNS = [
    (re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._-]+"), "authorization: Bearer ***"),
    (re.compile(r"(?i)password\s*=\s*[^&\s]+"), "password=***"),
    (re.compile(r"(?i)secret([^A-Za-z0-9]|$)"), "secret***"),
]

def redact(text: str) -> str:
    if not isinstance(text, str):
        return text
    out = text
    for pattern, repl in SIMPLE_PATTERNS:
        out = pattern.sub(repl, out)
    return out
