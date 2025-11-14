## Supply-chain autopatch prototype

**Why this matters (1 sentence):** Implements *Transparency → Validity → Separation* with an OSV-driven autopatch loop. :contentReference[oaicite:3]{index=3}

### How to run locally
```bash
python -m venv .venv
source .venv/bin/activate      # (Windows: .\.venv\Scripts\activate)
pip install -r sca-autopatch/requirements.txt
python -m autopatch.cli plan -r requirements.txt -o plan.csv
python -m autopatch.cli apply -r requirements.txt -p plan.csv   # (if plan shows fixes)
