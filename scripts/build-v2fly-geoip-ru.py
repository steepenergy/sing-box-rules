
import ipaddress
import json
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "v2fly/geoip/release/text/ru.txt"
)

with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
    text = response.read().decode("utf-8")

cidrs = []

for line in text.splitlines():
    line = line.strip()

    if not line or line.startswith("#"):
        continue

    # Reject malformed entries rather than silently skipping them.
    network = ipaddress.ip_network(line, strict=False)
    cidrs.append(str(network))

cidrs = sorted(set(cidrs))

if not cidrs:
    raise RuntimeError("No CIDRs found in v2fly ru.txt")

output = {
    "version": 3,
    "rules": [
        {
            "ip_cidr": cidrs
        }
    ]
}

Path("v2fly-geoip-ru.json").write_text(
    json.dumps(output, indent=2) + "\n",
    encoding="utf-8"
)

print(f"Generated {len(cidrs)} CIDR entries")
