# 📖 Panduan Penggunaan Detail

## Persiapan Lingkungan

### Windows (OSGeo4W)

```bash
# Buka OSGeo4W Shell sebagai Administrator
python -m pip install scikit-learn numpy
```

### Linux / macOS

```bash
# Dari terminal QGIS Python environment
pip3 install scikit-learn numpy
```

---

## Mempersiapkan Citra Sentinel-2

1. Download citra dari [Copernicus Open Access Hub](https://scihub.copernicus.eu/) atau [EarthExplorer](https://earthexplorer.usgs.gov/)
2. Gunakan Level-2A (sudah terkoreksi atmosfer)
3. Pisahkan Band 4 dan Band 8 sebagai file GeoTIFF terpisah
4. Pastikan kedua band berada dalam proyeksi koordinat yang sama

### Contoh memisahkan band menggunakan GDAL:

```bash
gdal_translate -b 4 input_sentinel2.tif band4_red.tif
gdal_translate -b 8 input_sentinel2.tif band8_nir.tif
```

---

## Mempersiapkan Data Sampel Lapangan

File vektor harus berupa **titik (Point)** dengan atribut minimal:

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `AGB` | Float | Above Ground Biomass (ton/ha) |

### Cara menghitung AGB dari data lapangan:

Gunakan persamaan allometrik Komiyama et al. (2005) untuk mangrove:

```
AGB = 0.251 × ρ × D^2.46
```

Dimana:
- `ρ` = densitas kayu (g/cm³), rata-rata mangrove = 0.7
- `D` = diameter batang setinggi dada/DBH (cm)

---

## Troubleshooting

### Error: "scikit-learn belum terinstall"

```bash
# Windows OSGeo4W Shell (sebagai Administrator)
python -m pip install scikit-learn

# Atau menggunakan pip3
pip3 install --user scikit-learn
```

### Error: "Sampel terlalu sedikit"

Plugin memerlukan minimal **5 titik sampel valid**. Pastikan:
- Semua titik berada dalam area citra (tidak di luar extent)
- Tidak ada nilai NULL pada kolom AGB
- Nama kolom AGB sesuai dengan yang diketikkan di parameter

### Hasil prediksi terlalu rendah/tinggi

- Periksa satuan AGB — harus dalam **ton/ha**, bukan kg/ha atau lainnya
- Periksa apakah citra sudah terkoreksi atmosfer (Level-2A)
- Tambah jumlah sampel lapangan untuk meningkatkan akurasi model

---

## Tips Meningkatkan Akurasi

1. **Jumlah sampel** — Minimal 30 titik sampel untuk hasil yang lebih stabil
2. **Distribusi sampel** — Sebaran spasial merata di seluruh area kajian
3. **Stratifikasi** — Ambil sampel dari berbagai kelas kerapatan mangrove
4. **Tanggal akuisisi** — Gunakan citra dari tanggal mendekati pengukuran lapangan
