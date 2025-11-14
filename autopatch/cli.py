from __future__ import annotations
import argparse, csv, sys
from typing import List, Tuple
from .utils import parse_requirements
from .osv_client import query_pypi
from .resolver import decide_fix
from .apply import apply_plan

def plan(req: str, out_csv: str) -> int:
    rows: List[Tuple[str, str, str, str]] = []  # name, current, fix, cves
    for name, version in parse_requirements(req):
        vulns = query_pypi(name, version)
        fix, cves = decide_fix(name, version, vulns)
        rows.append((name, version, fix or "", ";".join(cves)))
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "current", "fix_version", "vulns"])
        w.writerows(rows)
    print(f"Wrote {out_csv} with {len(rows)} rows")
    # return number of rows with a fix
    return sum(1 for r in rows if r[2])

def main():
    ap = argparse.ArgumentParser(prog="autopatch", description="OSV-driven autopatch for PyPI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("plan", help="create plan.csv from requirements.txt")
    p1.add_argument("-r", "--requirements", default="requirements.txt")
    p1.add_argument("-o", "--output", default="plan.csv")

    p2 = sub.add_parser("apply", help="apply plan.csv to requirements.txt")
    p2.add_argument("-r", "--requirements", default="requirements.txt")
    p2.add_argument("-p", "--plan", default="plan.csv")

    args = ap.parse_args()
    if args.cmd == "plan":
        changed = plan(args.requirements, args.output)
        # surface an exit code so CI can branch on it
        sys.exit(0 if changed == 0 else 10)

    elif args.cmd == "apply":
        import csv
        updates = []
        with open(args.plan, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("fix_version"):
                    updates.append((row["package"], row["fix_version"]))
        if not updates:
            print("No updates in plan.csv")
            return
        apply_plan(args.requirements, updates)
        print(f"Updated {args.requirements} with {len(updates)} fixes")

if __name__ == "__main__":
    main()
