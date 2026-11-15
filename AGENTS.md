# Beneath the Smoke — instructions for all AI coding agents

## Mission
Build an accessible public-facing, single-study-area, interactive web story about the 2026 fires in West Kalimantan. Central theme: compare NISAR L-band GCOV radar observations with independently mapped burned areas and FIRMS thermal detections. This is a time-boxed one-day NASA Space Apps prototype.

## Nonnegotiable scientific integrity rules
- NEVER invent a NISAR scene/granule ID, date, observation, fire perimeter, burned area, hotspot count, or statistics.
- A verified 2026 NISAR pre/post pair DOES NOT YET EXIST in project evidence; do not claim it does. Only enable radar-change layers when acquisition track, viewing geometry, polarization, spatial overlap, processing release, and quality masks are checked.
- A single GCOV observation is NOT a change measurement. Label it as a radar observation only.
- NISAR measures radar scattering, NOT peat-fire combustion, forest loss percentage, or vegetation recovery directly.
- FIRMS points are thermal detections, NOT individual fires or exact burned polygons.
- Burned-area products must be named with producer, month, method, caveats, and citation. Do not infer areas from arbitrary colours.
- Do not equate backscatter change with verified burn severity; atmosphere, wetness, topography, incidence geometry, and vegetation can influence measurements.
- Never fill gaps with plausible-looking fake measurements or map features. Use an honest empty state.

## Source of truth
- `docs/PROJECT_BRIEF.md` — scope and product.
- `docs/DATA_CONTRACT.md` — schema shared by frontend and preprocessing.
- `docs/STATUS.md` — which datasets are confirmed and what is actually implemented.
- `docs/SCIENCE_CHECKLIST.md` — validation gate.
- `public/data/ketapang/manifest.json` — machine-readable application data availability. Initially unverified.

## Implementation
- Frontend: React, TypeScript, Vite, MapLibre. Prefer a static site with precomputed geographic overlays and small JSON files.
- Data: Python scripts under `scripts/`. Put raw data in `data/raw/` (gitignored), derived large data in `data/processed/` (gitignored).
- Prefer transparent georeferenced overlays, validated coordinate bounds, one regional case study, and no backend.
- Keep changes small and reviewable; no dependency installation or git push unless the user authorizes it.
- Before changing code, read relevant docs and `docs/STATUS.md`. Report files changed, commands run, results, and unresolved issues.
- Avoid touching another agent's scope without asking. Data agent: scripts/data/docs source evidence. Frontend agent: src/public display. Reviewer agent: read-only.

## Testing
- Frontend: `npm run build`; additionally inspect app in browser.
- Data discovery: `python scripts/check_data.py` only with internet; output is metadata candidates, not confirmed scenes.
- For each real raster: validate CRS, geographic bounds, pixel alignment, units, no-data, and source metadata.
- Never claim a tool or test ran unless it actually ran.
