# 📁 Sample Data

Folder ini untuk menyimpan data sampel pengujian.

## Format yang Didukung

- **Shapefile** (`.shp`): format klasik ESRI
- **GeoPackage** (`.gpkg`): format modern, disarankan
- **GeoJSON** (`.geojson`): untuk kolaborasi berbasis web

## Struktur Atribut Minimum

```
FID | geometry (Point) | AGB (float)
```

## Contoh Data

Gunakan skrip `scripts/generate_sample_data.py` untuk membuat data dummy:

```bash
python scripts/generate_sample_data.py
```

Output: `sample_data/sample_points_dummy.geojson`

> ⚠️ Jangan commit data koordinat GPS lapangan aktual ke repository publik
> tanpa izin dari pemilik data.
