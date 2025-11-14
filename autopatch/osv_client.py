# Minimal OSV client for PyPI
from __future__ import annotations
from typing import Dict, List
import requests

OSV_QUERY_URL = "https://api.osv.dev/v1/query"

def query_pypi(name: str, version: str) -> List[Dict]:
    payload = {"package": {"name": name, "ecosystem": "PyPI"}, "version": version}
    r = requests.post(OSV_QUERY_URL, json=payload, timeout=20)
    r.raise_for_status()
    return r.json().get("vulns", []) or []

def fixed_versions_for(name: str, vulns: List[Dict]) -> List[str]:
    fixes = []
    lower = name.lower()
    for v in vulns:
        for aff in v.get("affected", []):
            pkg = (aff.get("package") or {}).get("name", "")
            if pkg and pkg.lower() != lower:
                continue
            for rng in aff.get("ranges", []):
                for ev in rng.get("events", []):
                    if "fixed" in ev:
                        fixes.append(ev["fixed"])
    return sorted(set(fixes))
