
import json
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "v2fly/geoip/release/text/ru.txt"
)

with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
    text = response.read().decode("utf-8")

cidrs = sorted({
    line.strip()
    for line in text.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
})

if not cidrs:
    raise RuntimeError("Source contains no CIDR ranges")

# Validate every network before generating the rule-set.
import ipaddress

for cidr in cidrs:
    ipaddress.ip_network(cidr, strict=False)

data = {
    "version": 3,
    "rules": [
        {
            "ip_cidr": cidrs
        }
    ]
}

Path("geoip-ru.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)

print(f"Generated geoip-ru.json with {len(cidrs)} CIDRs")
