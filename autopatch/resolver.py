from __future__ import annotations
from typing import Dict, List, Tuple
from .utils import min_higher_version
from .osv_client import fixed_versions_for

def decide_fix(name: str, cur_ver: str, vulns: List[Dict]) -> Tuple[str | None, List[str]]:
    """Return (best_fix_version, cve_list)."""
    cves = [a for a in {a.get("id","") for a in vulns} if a]
    fix_candidates = fixed_versions_for(name, vulns)
    best = min_higher_version(cur_ver, fix_candidates) if fix_candidates else None
    return best, cves
