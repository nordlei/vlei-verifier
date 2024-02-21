import json
import os
from datetime import datetime, timezone

timestamp = datetime.now(timezone.utc).isoformat(timespec='microseconds')

config = json.dumps({
  "dt": timestamp,
  "iurls": list(filter(len, (os.getenv("WITNESS_URL") or "").split(";"))),
  "durls": list(filter(len, (os.getenv("SCHEMA_URL") or "").split(";"))),
}, indent=2)

print(config)
