import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import './App.css';

type Manifest = {
  project: string;
  studyArea: {
    label: string;
    center: [number, number];
    bounds: [number, number, number, number] | null;
    status: string;
  };
  event: { label: string; startDate: string | null; endDate: string | null; status: string };
  radar: { status: string; sensor: string; product: string; radarChangeAvailable: boolean; notes: string };
  layers: Array<{ id: string; label: string; status: string; url: string }>;
};

const MAP_STYLE = 'https://demotiles.maplibre.org/style.json';
const DEFAULT_CENTER: [number, number] = [109.97, -1.83];

export default function App() {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/data/ketapang/manifest.json')
      .then((r) => {
        if (!r.ok) throw new Error(`Could not load manifest (${r.status})`);
        return r.json() as Promise<Manifest>;
      })
      .then(setManifest)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'Manifest loading failed'));
  }, []);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: MAP_STYLE,
      center: DEFAULT_CENTER,
      zoom: 8,
      attributionControl: false,
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'top-right');
    map.addControl(new maplibregl.AttributionControl({ compact: true }), 'bottom-right');
    mapRef.current = map;
    return () => { map.remove(); mapRef.current = null; };
  }, []);

  const verifiedLayers = manifest?.layers.filter((layer) => layer.status === 'verified').length ?? 0;

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="mark">✺</span><div><strong>Beneath the Smoke</strong><small>INDONESIA · 2026</small></div></div>
        <a href="https://nisar.jpl.nasa.gov/" target="_blank" rel="noreferrer" className="nav-link">About NISAR ↗</a>
      </header>
      <section className="layout">
        <aside className="story">
          <p className="eyebrow">NASA SPACE APPS · EARTH OBSERVATIONS</p>
          <h1>What remains <em>after the fire?</em></h1>
          <p className="intro">An interactive story about the 2026 fires in West Kalimantan—and what radar can teach us about the landscape.</p>
          <div className="rule"/>
          <p className="eyebrow">01 / START HERE</p>
          <h2>Follow the evidence</h2>
          <p className="body">We will combine independently mapped burned areas, satellite thermal detections, and NASA's NISAR radar observations. Each source measures something different.</p>
          <div className="statusBox">
            <div className="statusDot"/><div><strong>Data verification in progress</strong>
            <p>No specific NISAR scene or before/after pair has been verified for this location yet. We will not show simulated fire or radar measurements as real observations.</p></div>
          </div>
          <div className="facts">
            <div><span>STUDY REGION</span><strong>{manifest?.studyArea.label ?? 'Ketapang, West Kalimantan'}</strong></div>
            <div><span>VERIFIED MAP LAYERS</span><strong>{verifiedLayers}</strong></div>
            <div><span>NISAR CHANGE ANALYSIS</span><strong>{manifest?.radar.radarChangeAvailable ? 'Available' : 'Not yet validated'}</strong></div>
          </div>
          {error && <p className="error" role="alert">{error}</p>}
          <a className="guide" href="https://nisar-docs.asf.alaska.edu/" target="_blank" rel="noreferrer">How NISAR radar works ↗</a>
        </aside>
        <section className="mapArea" aria-label="Interactive regional basemap">
          <div className="map" ref={containerRef}/>
          <div className="mapLabel"><span className="mapLabelDot"/> STARTING LOCATION · NOT A VERIFIED FIRE FOOTPRINT</div>
          <div className="floatingLegend"><strong>Map status</strong><p>Basemap only. Verified satellite overlays will be added after the scientific checks.</p></div>
        </section>
      </section>
      <footer className="footer">A scientific prototype. Approximate city-centre camera only. Map tiles: MapLibre demo service (replace for production).</footer>
    </main>
  );
}
