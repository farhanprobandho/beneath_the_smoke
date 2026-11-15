# Shared data contract (v0.1)

The frontend reads `public/data/ketapang/manifest.json` as `/data/ketapang/manifest.json`.

Required top-level fields:
- `project`: string
- `studyArea`: `{label, center: [longitude, latitude], bounds: null | [west, south, east, north], status}`
- `event`: `{label, startDate, endDate, status}`; dates are ISO `YYYY-MM-DD` and may be `null` until verified
- `radar`: `{status, sensor, product, polarization, beforeDate, afterDate, radarChangeAvailable, sourceUrl, notes}`
- `layers`: array of `{id, type, label, url, bounds, acquisitionDate, source, units, status}`; verified items only. `bounds` is `[west,south,east,north]` for documentation, or translate to the MapLibre image-source corner order programmatically.
- `updatedUtc`: `null` or ISO timestamp

Allowed `status` values: `unverified`, `verified`, `unavailable`. Do not store example/fictional entries in `layers`.

MapLibre `image` source coordinates are **top-left, top-right, bottom-right, bottom-left**, each `[longitude, latitude]`.

Numeric analysis remains in the Python dataset. Map images are visual displays only; do not use pixel colours as measurement truth. When later adding clickable measurements, include the acquisition dates, band, statistic, unit, valid-pixel count, and exact spatial region.

Do not add frontend default granule dates or burn-area statistics. `null` means not established, not zero.
