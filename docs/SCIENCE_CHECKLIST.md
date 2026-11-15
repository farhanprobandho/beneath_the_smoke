# Scientific acceptance checklist

## Before claiming NISAR coverage
- [ ] Exact granule/scene ID and ASF source link recorded.
- [ ] Acquisition timestamp verified.
- [ ] Scene polygon intersects an independently verified fire footprint (not merely a broad Ketapang search box).
- [ ] Requested polarization layer exists in the actual data.
- [ ] Quality mask and coverage inspected.

## Before computing radar change
- [ ] Confirm pre and post observations straddle the relevant event.
- [ ] Same compatible viewing geometry, track/direction, polarization, frequency, and processing maturity/version.
- [ ] Handle incidence/terrain/land-water differences and known calibration caveats.
- [ ] Reproject and align pixel grids with correct transforms and valid-data masks.
- [ ] Use `10 * log10(linear_power)` only for finite, positive power; avoid directly averaging dB values where linear-power averaging is intended.
- [ ] Compare inside burned area to a sensible unburned reference; test if wider non-fire changes suggest moisture effects.
- [ ] State that backscatter change does not uniquely imply burning or recovery.

## Before displaying fire datasets
- [ ] Distinguish FIRMS thermal detections from fire incidents and burn boundaries.
- [ ] Verify MapBiomas/alternate file is actually available and inspect spatial resolution, coding, NoData, and licensing.
- [ ] Use a projected CRS/equal-area method for area calculations.
- [ ] Source all figures and identify geographic extent and date ranges.

## Before release
- [ ] All layers align with the basemap and each other.
- [ ] Dates, uncertainty, sources and units are clearly visible.
- [ ] No placeholder appears as a scientific measurement.
- [ ] Frontend builds and basic interactions work.
