from __future__ import annotations
from typing import List, Tuple
from .utils import write_requirements

def apply_plan(req_path: str, updates: List[Tuple[str, str]]) -> None:
    # updates: [(name, new_version), ...]
    lines = []
    # Build map for quick update
    upd = {n.lower(): v for n, v in updates}
    with open(req_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if "==" in line and not line.startswith("#"):
                name, cur = [x.strip() for x in line.split("==", 1)]
                nv = upd.get(name.lower())
                if nv:
                    lines.append(f"{name}=={nv}\n")
                else:
                    lines.append(f"{name}=={cur}\n")
            else:
                lines.append(raw)
    with open(req_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
