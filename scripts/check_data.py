#!/usr/bin/env python3
"""Reproducible NISAR GCOV / Ketapang 2026 archive feasibility check.

Not a wildfire mapping or calibration pipeline. Tests *catalogue metadata* and
public supporting data. No invented imagery or scene statistics.

Usage:
  pip install -U asf_search requests
  python check_data.py
  python check_data.py --bbox 109.5,-2.3,110.5,-1.2

Outputs in ./results/: scenes.csv, same_track_pairs.csv, report.json,
optional worldfires_points.csv. The AOI is only a screening rectangle.
"""
from __future__ import annotations
import argparse
import collections
import csv
import datetime as dt
import io
import json
import math
import re
from pathlib import Path

import requests

# A documented candidate event, NOT a vetted ground-confirmed fire perimeter.
EVENT_URL = "https://worldfires.org/en/fire/ketapang-2026-09-12"
# Public link exposed by the event's "Download CSV" control as of 2026-11-14.
EVENT_CSV_URL = "https://worldfires.org/en/api/detecciones/407870?csv=1"
MAPBIOMAS_PREFIX = (
    "https://storage.googleapis.com/mapbiomas-public/initiatives/indonesia/"
    "fire/monitor/mapbiomas_fire_monthly_burned_v1/"
)
DEFAULT_BBOX = [109.45, -2.45, 110.55, -1.05]  # exploratory Ketapang region, not fire bounds
FIRE_START = dt.date(2026, 9, 16)
FIRE_END = dt.date(2026, 9, 27)


def bbox_wkt(bounds):
    w, s, e, n = bounds
    return f"POLYGON(({w} {s},{e} {s},{e} {n},{w} {n},{w} {s}))"


def parse_name(name):
    """Parse NISAR L2 GCOV naming convention, not scene internals."""
    parts = (name or "").replace(".h5", "").split("_")
    if len(parts) < 17 or parts[0] != "NISAR" or parts[3] != "GCOV":
        return {}
    return {
        "band": parts[1], "processing_type": parts[2],
        "cycle": parts[4], "relative_track": parts[5],
        "direction": parts[6], "frame": parts[7],
        "bandwidth_code": parts[8], "polarization_code": parts[9],
        "source_code": parts[10], "start_utc": parts[11],
        "end_utc": parts[12], "release_id": parts[13],
    }


def check_object(session, url):
    """HEAD then tiny ranged GET; never download the national GeoTIFF."""
    info = {"url": url, "status": "unverified"}
    try:
        r = session.head(url, timeout=18, allow_redirects=True)
        info["head_http"] = r.status_code
        info["content_type"] = r.headers.get("Content-Type")
        info["bytes"] = r.headers.get("Content-Length")
        if r.status_code == 200:
            info["status"] = "object_exists_head_200"
            return info
        if r.status_code in (403, 404):
            info["status"] = f"head_http_{r.status_code}"
            if r.status_code == 404:
                return info
    except requests.RequestException as exc:
        info["head_error"] = f"{type(exc).__name__}: {exc}"
    try:
        with session.get(url, headers={"Range": "bytes=0-15"}, timeout=18, stream=True) as r:
            info["get_http"] = r.status_code
            info["content_type"] = r.headers.get("Content-Type")
            if r.status_code in (200, 206):
                # Stream only a few bytes, then close. Do NOT fetch a nationwide TIFF.
                first = next(r.iter_content(chunk_size=16), b"")
                info["header_bytes_hex"] = first[:4].hex()
                info["status"] = "object_exists_get_200_or_206"
            else:
                info["status"] = f"get_http_{r.status_code}"
    except requests.RequestException as exc:
        info["get_error"] = f"{type(exc).__name__}: {exc}"
    return info


def download_event_points(session, output):
    report = {"source": EVENT_URL, "csv_url": EVENT_CSV_URL,
              "status": "not_checked", "rows": 0}
    try:
        response = session.get(EVENT_CSV_URL, timeout=25)
        report["http"] = response.status_code
        response.raise_for_status()
        if "text/html" in response.headers.get("Content-Type", ""):
            raise ValueError("CSV endpoint returned HTML")
        data = response.text.lstrip("\ufeff")
        reader = csv.DictReader(io.StringIO(data))
        rows = list(reader)
        if not rows:
            raise ValueError("Empty CSV")
        report["columns"] = list(rows[0])
        report["rows"] = len(rows)
        report["status"] = "csv_downloaded_not_independently_verified"
        (output / "worldfires_points.csv").write_text(data, encoding="utf-8")
        # This is a secondary republisher, not the native FIRMS archive.
        lat_keys = ["lat", "latitude", "latitud"]
        lon_keys = ["lon", "lng", "longitude", "longitud"]
        names = {x.lower():x for x in rows[0]}
        lat = next((names[k] for k in lat_keys if k in names), None)
        lon = next((names[k] for k in lon_keys if k in names), None)
        if lat and lon:
            pts = []
            for row in rows:
                try:
                    x, y = float(row[lon]), float(row[lat])
                    if -180 <= x <= 180 and -90 <= y <= 90:
                        pts.append((x, y))
                except (TypeError, ValueError, KeyError):
                    pass
            if pts:
                report["points_with_coordinates"] = len(pts)
                report["bbox_of_points"] = [min(p[0] for p in pts), min(p[1] for p in pts),
                                            max(p[0] for p in pts), max(p[1] for p in pts)]
        return report
    except (requests.RequestException, ValueError) as exc:
        report["status"] = "not_accessible"
        report["error"] = f"{type(exc).__name__}: {exc}"
        return report


def query_nisar(bounds, max_results):
    import asf_search as asf  # installed by the user, supported by ASF
    options = asf.ASFSearchOptions(
        dataset=["NISAR"], processingLevel=["GCOV"],
        productionConfiguration=["PR"], dataMaturity="PROVISIONAL",
        intersectsWith=bbox_wkt(bounds),
        start=dt.datetime(2026, 6, 17), end=dt.datetime(2026, 10, 20),
        maxResults=max_results,
    )
    results = asf.search(opts=options)
    entries = []
    for scene in results:
        p = scene.properties
        label = str(p.get("sceneName") or p.get("fileID") or "")
        parsed = parse_name(label)
        if not parsed or parsed.get("band") != "L2":
            continue
        row = {
            "scene_name": label, "acquisition_start": str(p.get("startTime", "")),
            "acquisition_end": str(p.get("stopTime", "")),
            "url": p.get("url", ""),
            "catalog_polarization": str(p.get("polarization") or ""),
            "catalog_path": str(p.get("pathNumber") or ""),
            "catalog_frame": str(p.get("frameNumber") or ""),
            "data_maturity_requested": "PROVISIONAL",
            **parsed,
        }
        entries.append(row)
    return entries


def make_pairs(rows):
    """Candidate metadata matches; requires manual spatial and raster checks."""
    groups = collections.defaultdict(list)
    for row in rows:
        key = tuple(row.get(k) for k in
                    ("relative_track", "direction", "frame", "bandwidth_code",
                     "polarization_code", "release_id"))
        groups[key].append(row)
    pairs = []
    for group in groups.values():
        pre = [r for r in group if r.get("start_utc", "")[:8] < FIRE_START.strftime("%Y%m%d")]
        post = [r for r in group if r.get("start_utc", "")[:8] > FIRE_END.strftime("%Y%m%d")]
        for before in pre:
            for after in post:
                pairs.append({
                    "before_date": before.get("start_utc"),
                    "after_date": after.get("start_utc"),
                    "before_scene": before.get("scene_name"),
                    "after_scene": after.get("scene_name"),
                    "relative_track": before.get("relative_track"),
                    "direction": before.get("direction"),
                    "frame": before.get("frame"),
                    "bandwidth_code": before.get("bandwidth_code"),
                    "polarization_code": before.get("polarization_code"),
                    "release_id": before.get("release_id"),
                    "warning": "METADATA CANDIDATE ONLY: verify footprint overlap, modes, masks, temporal surface stability, and actual imagery",
                })
    return sorted(pairs, key=lambda r: (r["after_date"], r["before_date"]))


def write_csv(path, rows):
    if not rows:
        path.write_text("No matching rows found. See report.json.\n", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bbox", default=",".join(map(str, DEFAULT_BBOX)),
                        help="west,south,east,north — exploratory area, not an observed burn perimeter")
    parser.add_argument("--max-results", type=int, default=500)
    parser.add_argument("--output", default="results")
    parser.add_argument("--skip-worldfires", action="store_true")
    args = parser.parse_args()
    bounds = [float(x) for x in args.bbox.split(",")]
    if len(bounds) != 4 or not (bounds[0] < bounds[2] and bounds[1] < bounds[3]):
        parser.error("--bbox must be west,south,east,north")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "SpaceApps-Ketapang-Feasibility/1.0"})
    report = {
        "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "study_area": "exploratory Ketapang screening area (not an event perimeter)",
        "bbox_wsen": bounds, "bbox_wkt": bbox_wkt(bounds),
        "target_event": EVENT_URL,
        "event_start": FIRE_START.isoformat(), "event_end": FIRE_END.isoformat(),
        "dataset": "NISAR L2 GCOV PROVISIONAL",
        "caution": "Metadata candidates are not validated radar backscatter changes.",
    }
    if not args.skip_worldfires:
        report["republished_firms_detections"] = download_event_points(session, output)
        print("WorldFires CSV:", report["republished_firms_detections"]["status"])
    for month in ("08", "09"):
        url = MAPBIOMAS_PREFIX + f"monthly_burned-indonesia_2026_{month}.tif"
        report[f"mapbiomas_2026_{month}"] = check_object(session, url)
        print(f"MapBiomas {month}:", report[f"mapbiomas_2026_{month}"]["status"])
    try:
        scenes = query_nisar(bounds, args.max_results)
        report["nisar_catalog_status"] = "query_succeeded"
        report["nisar_scene_count"] = len(scenes)
        report["nisar_scenes_with_dh_polarization_code"] = sum(
            r.get("polarization_code", "")[:2] == "DH" for r in scenes)
        pairs = make_pairs(scenes)
        report["metadata_pair_candidates"] = len(pairs)
        write_csv(output / "scenes.csv", scenes)
        write_csv(output / "same_track_pairs.csv", pairs)
        print("NISAR scenes:", len(scenes), "metadata pair candidates:", len(pairs))
        if len(scenes) >= args.max_results:
            report["catalog_warning"] = "Search may be truncated by max-results; use tighter bbox."
    except Exception as exc:
        report["nisar_catalog_status"] = "query_failed"
        report["nisar_catalog_error"] = f"{type(exc).__name__}: {exc}"
        print("NISAR query failed:", report["nisar_catalog_error"])
    (output / "report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("Wrote", (output / "report.json").resolve())
    print("A matched scene pair still requires scene-level polarization, image, and footprint verification.")

if __name__ == "__main__":
    main()
