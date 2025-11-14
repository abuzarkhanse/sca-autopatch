# Supply‑chain Autopatch Prototype (SBOM → OSV → Signed Evidence)

![Auto‑patch CVEs](https://github.com/abuzarkhanse/sca-autopatch/actions/workflows/autopatch.yml/badge.svg)

This repository implements a minimal, repeatable pipeline that demonstrates the **Transparency → Validity → Separation** design properties for secure software supply chains by generating a signed SBOM, scanning it with OSV, and opening an auto‑patch PR with evidence.

---

## What the pipeline does

1. **Plan updates** from OSV “fixed” info → `plan.csv`.
2. **Generate SBOM** (CycloneDX via `cdxgen`) → `sbom.cdx.json`.
3. **Scan SBOM with OSV‑Scanner** (Docker) → `reports/osv-report.json`.
4. **Sign SBOM** (Sigstore cosign, keyless OIDC) → `sbom.sig`, `sbom.cert`.
5. **Verify signature** (cosign v2 with identity checks).
6. **Reproducibility smoke test** (`pip freeze` twice) → `reports/reproducibility.diff`.
7. **Open a PR** with the minimum safe versions when fixes exist.
8. **Upload evidence** as artifacts (`autopatch-reports`).

**Why this matters (SoK mapping):**
- **Transparency:** SBOM + OSV report + metrics give visibility into artifacts/operations. SBOMs and dependency analysis are called out as transparency techniques in the SoK. :contentReference[oaicite:0]{index=0}
- **Validity:** Cosign keyless signatures and verification (with OIDC identity) provide artifact/operation integrity; reproducibility is recommended evidence of integrity. :contentReference[oaicite:1]{index=1}
- **Separation:** CI runs on an ephemeral runner; OSV‑Scanner is containerized; changes land via PR (no in‑place edits), aligning with the SoK’s separation guidance. :contentReference[oaicite:2]{index=2}

---

## Run locally (CLI)

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .\.venv\Scripts\activate

pip install -r requirements.txt
python -m autopatch.cli plan  -r requirements.txt -o plan.csv
# Optional (applies the plan to requirements.txt):
python -m autopatch.cli apply -r requirements.txt -p plan.csv
