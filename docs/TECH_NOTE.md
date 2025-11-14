# SCA AutoPatch – Research Alignment

This prototype implements the **Transparency → Validity → Separation** design properties from the SoK by Okafor et al. (Purdue). :contentReference[oaicite:2]{index=2}

## Pipeline → Properties

- **Transparency:** CycloneDX SBOM (`sbom.cdx.json`), OSV report (`reports/osv-report.json`).
- **Validity:** SBOM **signed + verified** with Sigstore (`sbom.sig`, `sbom.cert`); reproducibility diff (`reports/reproducibility.diff`).
- **Separation:** Ephemeral CI runners; automated evidence artifacts.

## Metrics to report

- Packages scanned; packages with fixes (`reports/metrics.json`).
- Time from “scan” to “PR opened” (use GitHub run timestamps).
