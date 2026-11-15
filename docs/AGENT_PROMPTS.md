# Copy-and-paste prompts for agent sessions

## 1 — Planner
Read AGENTS.md and docs/STATUS.md. Give me the two smallest independent next tasks that most reduce scientific and delivery risk. Do not change files. Each task must have an owner, exact files and a testable acceptance criterion.

## 2 — Data Scientist: discovery
Read AGENTS.md, docs/SCIENCE_CHECKLIST.md, docs/DATA_CONTRACT.md and scripts/check_data.py. Run the checker if network access is available. Explain any API errors; do not infer absence of coverage from request failure. Report exact candidate granule names, footprints (after verifying them), acquisition dates and track/polarization metadata. Save evidence and update docs/STATUS.md. Do not build change maps until pair suitability is demonstrated. Do not edit src/.

## 3 — Frontend Engineer: first task
Read AGENTS.md, docs/PROJECT_BRIEF.md, docs/DATA_CONTRACT.md and the manifest. Make the starter MapLibre map attractive, responsive and accessible, but do not invent data. Keep its honest "NISAR not yet verified" message. Implement a reusable layer component that supports a verified GeoJSON source when an entry appears in the manifest. Run npm run build and list any errors. Do not edit scripts/.

## 4 — Reviewer
Review recent changes against AGENTS.md and docs/SCIENCE_CHECKLIST.md. Identify errors and unsupported data claims with file paths and severity. Do not edit code. If tests cannot be run, do not imply they passed.

## Follow-up after each agent task
Show me a concise summary of changed files, commands/tests run (with actual output), outstanding risks, and one recommended next task. Stop before changing unrelated files.
