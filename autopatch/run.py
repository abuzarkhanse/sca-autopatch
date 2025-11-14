# autopatch/run.py
import subprocess
from autopatch.apply import apply_from_plan

def run_shell(cmd):
    print(f"$ {cmd}")
    return subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    # 1) plan (already done in Phase 2)
    # 2) apply upgrades
    apply_from_plan("plan.csv", "requirements.txt")
    # 3) (optional) run tests if the repo has them
    #    we'll just try pytest if it exists
    try:
        run_shell("pytest -q")
    except Exception:
        print("pytest not found or tests failed; skipping")
