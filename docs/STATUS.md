# Project status — update this after each task

## Data, as of initial repo creation
- NISAR Provisional GCOV *collection* exists for 2026. Exact Ketapang scene footprint: **UNVERIFIED**.
- Compatible before/after NISAR pair over a selected 2026 fire: **UNVERIFIED**.
- Actual available polarization in a matching scene: **UNVERIFIED**.
- Public reporting documents fires in West Kalimantan in 2026; exact selected fire footprint: **UNVERIFIED IN THIS REPO**.
- September 2026 MapBiomas downloadable georeferenced raster: **UNVERIFIED**.
- Historical FIRMS events can be sought; actual filtered hotspot dataset: **NOT YET LOADED**.

## Implemented
- Minimal React + MapLibre map with an honest unverified-data state.
- Project rules, role agents, discovery checker, and data contract.

## Next tasks
1. Data Scientist: run `scripts/check_data.py` online; inspect results and log actual scene IDs and timestamps; do not call candidate pairs validated.
2. Data Scientist: determine exact fire footprint + data access; revise study area bounds with real evidence.
3. Frontend Engineer: connect verified GeoJSON and image overlays from manifest, retaining missing-data states.
4. Reviewer: audit sources and build after each substantive change.

## Work log
- [initial] Starter repo created; all scientific findings remain unverified until live checks and image inspection.
