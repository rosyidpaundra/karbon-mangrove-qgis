"""
generate_sample_data.py
-----------------------
Membuat data titik sampel dummy untuk pengujian plugin AGC Mangrove.
Output: sample_data/sample_points_dummy.geojson

Jalankan:
    python scripts/generate_sample_data.py
"""

import json
import random
import math
import os

# ── Konfigurasi ───────────────────────────────────────────────────────────────
# Pusat area (ubah sesuai lokasi kajian Anda)
CENTER_LON = 110.3695   # Longitude pusat (contoh: Yogyakarta)
CENTER_LAT = -7.7956    # Latitude pusat
SPREAD     = 0.05       # Sebaran titik dalam derajat (~5 km)
N_POINTS   = 50         # Jumlah titik sampel

# Rentang AGB mangrove realistis (ton/ha)
AGB_MIN = 15.0
AGB_MAX = 120.0

random.seed(42)

# ── Buat GeoJSON ──────────────────────────────────────────────────────────────
features = []
for i in range(N_POINTS):
    # Distribusi titik melingkar acak
    angle  = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0, SPREAD)
    lon = CENTER_LON + radius * math.cos(angle)
    lat = CENTER_LAT + radius * math.sin(angle)

    # AGB dengan distribusi log-normal (lebih realistis)
    agb = round(random.lognormvariate(math.log(50), 0.5), 2)
    agb = max(AGB_MIN, min(AGB_MAX, agb))
    agc = round(agb * 0.47, 2)

    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [round(lon, 6), round(lat, 6)]
        },
        "properties": {
            "FID":  i + 1,
            "AGB":  agb,
            "AGC":  agc,
            "keterangan": f"Plot sampel #{i+1}"
        }
    })

geojson = {
    "type": "FeatureCollection",
    "name": "sample_agb_points",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
    },
    "features": features
}

# ── Simpan ────────────────────────────────────────────────────────────────────
out_dir  = os.path.join(os.path.dirname(__file__), "..", "sample_data")
out_path = os.path.join(out_dir, "sample_points_dummy.geojson")

os.makedirs(out_dir, exist_ok=True)

with open(out_path, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"✅ Berhasil membuat {N_POINTS} titik sampel dummy")
print(f"   Output: {os.path.abspath(out_path)}")
print(f"   Rentang AGB: {AGB_MIN} – {AGB_MAX} ton/ha")
