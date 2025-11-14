from __future__ import annotations
from typing import Dict, List, Tuple
import re
from packaging.version import Version # type: ignore


REQ_LINE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*==\s*([A-Za-z0-9_.+\-]+)\s*$")

def parse_requirements(path: str) -> List[Tuple[str, str]]:
    pkgs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = REQ_LINE.match(line.strip())
            if m:
                pkgs.append((m.group(1), m.group(2)))
    return pkgs

def write_requirements(path: str, rows: List[Tuple[str, str]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for name, ver in rows:
            f.write(f"{name}=={ver}\n")

def min_higher_version(current: str, candidates: List[str]) -> str | None:
    cur = Version(current)
    higher = [Version(v) for v in candidates if Version(v) > cur]
    return str(min(higher)) if higher else None
