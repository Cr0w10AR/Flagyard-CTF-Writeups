"""Parse recorded ModSecurity audit transactions for offline incident review."""
import re
from pathlib import Path
from urllib.parse import unquote_plus

_BOUNDARY = re.compile(r"(?m)(?=^--[0-9a-fA-F]+-A--$)")
_REQUEST = re.compile(r"(?m)^id=(.*)$")
_RESPONSE = re.compile(r"<pre>(.*?)</pre>", re.S)

def read_transactions(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    for tx in _BOUNDARY.split(raw):
        request = _REQUEST.search(tx)
        response = _RESPONSE.search(tx)
        if request and response:
            body = unquote_plus(request.group(1))
            message = response.group(1).strip()
            if message == "User ID exists in the database.":
                yield body, True
            elif message == "User ID is MISSING from the database.":
                yield body, False
