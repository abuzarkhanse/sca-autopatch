# Supply‑chain Autopatch Prototype (SBOM → OSV → Signed Evidence)

![Auto‑patch CVEs](https://github.com/abuzarkhanse/sca-autopatch/actions/workflows/autopatch.yml/badge.svg)

**Why this matters:** A minimal, repeatable pipeline that implements **Transparency → Validity → Separation** for Python projects by generating a signed SBOM, scanning it with OSV, and opening an auto‑patch PR with evidence.

---

## What this pipeline does

1. **Creates a plan** of dependency upgrades using OSV fixed‑version data (`plan.csv`).
2. **Generates an SBOM** (CycloneDX via `cdxgen`).
3. **Scans the SBOM** with **OSV‑Scanner** (Docker image).
4. **Signs the SBOM** with **Sigstore cosign (keyless/OIDC)** and **verifies** the signature.
5. **Performs a reproducibility smoke test** (`pip freeze` twice; stores diff).
6. **Opens a PR automatically** (minimum fixed versions) when fixes exist.
7. **Uploads evidence artifacts** for review.

**Evidence artifacts (Actions → run → “autopatch‑reports”):**
- `sbom.cdx.json` (CycloneDX)
- `sbom.sig`, `sbom.cert` (cosign signature & certificate)
- `reports/osv-report.json` (OSV scan results)
- `reports/reproducibility.diff`
- `reports/metrics.json`
- `plan.csv`

---

## Quickstart (local)

> You can test the CLI locally; CI remains the source of truth.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .\.venv\Scripts\activate

pip install -r requirements.txt
python -m autopatch.cli plan  -r requirements.txt -o plan.csv
# Optional (applies the plan to requirements.txt):
python -m autopatch.cli apply -r requirements.txt -p plan.csv

