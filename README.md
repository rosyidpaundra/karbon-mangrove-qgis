# 🌿 Karbon Mangrove QGIS — AGC Estimation Plugin

<p align="center">
  <img src="docs/banner.png" alt="Karbon Mangrove Banner" width="700"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/QGIS-3.x-green?logo=qgis&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-RandomForest-orange"/>
  <img src="https://img.shields.io/badge/Sentinel--2-Band%204%20%26%208-lightblue"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow"/>
</p>

---

## 📋 Deskripsi

Plugin QGIS berbasis **Python Processing Framework** untuk estimasi **Above Ground Carbon (AGC)** pada ekosistem hutan mangrove menggunakan algoritma **Random Forest Regressor**.

Plugin ini mengintegrasikan data spektral citra **Sentinel-2** (Band 4/Red & Band 8/NIR) dengan data sampel lapangan **Above Ground Biomass (AGB)** untuk menghasilkan peta prediksi stok karbon spasial.

### Alur Kerja Utama

```
Citra Sentinel-2        Titik Sampel Lapangan
  Band 4 (Red)    +       AGB (ton/ha)
  Band 8 (NIR)                │
        │                     │
        └────────┬────────────┘
                 │
        Ekstraksi Piksel
        (native:rastersampling)
                 │
        Hitung NDVI + Konversi AGC
        AGC = AGB × 0.47 (IPCC)
                 │
        Training Random Forest
        (n_estimators=100, test_size=30%)
                 │
        Prediksi Raster Full-Extent
                 │
        ┌────────┴────────────┐
   Peta AGC (GeoTIFF)   Laporan Statistik
   (Ton C / piksel)     (R², RMSE, Total C)
```

---

## 🚀 Fitur

- ✅ **Input fleksibel** — mendukung semua format raster GDAL & vektor OGR
- ✅ **NDVI otomatis** — dihitung langsung dari Band Red & NIR
- ✅ **Konversi AGC standar IPCC** — faktor 0.47 sesuai pedoman internasional
- ✅ **Evaluasi model** — R², RMSE, MAE dilaporkan di log QGIS
- ✅ **Prediksi row-by-row** — efisien untuk raster berukuran besar
- ✅ **Output GeoTIFF Float32** — kompatibel dengan semua GIS software
- ✅ **Laporan statistik karbon** — total luas, total AGC, rata-rata AGC/Ha

---

## 📦 Instalasi

### Prasyarat

| Komponen | Versi |
|----------|-------|
| QGIS | ≥ 3.16 |
| Python | ≥ 3.9 |
| scikit-learn | ≥ 1.0 |
| numpy | ≥ 1.21 |
| GDAL/OGR | ≥ 3.3 |

### Instalasi scikit-learn di OSGeo4W (Windows)

Buka **OSGeo4W Shell** sebagai Administrator:

```bash
python -m pip install scikit-learn
```

### Instalasi Plugin

1. Download atau clone repository ini:
   ```bash
   git clone https://github.com/USERNAME/karbon-mangrove-qgis.git
   ```

2. Copy folder `plugin/` ke direktori QGIS Processing Scripts:
   - Windows: `C:\Users\<nama>\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts\`
   - Linux/Mac: `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts/`

3. Buka QGIS → **Processing Toolbox** → Refresh Scripts

4. Plugin akan muncul di: **Analisis Karbon → Estimasi AGC dari AGB (RF Model)**

---

## 🗂️ Struktur Repository

```
karbon-mangrove-qgis/
├── plugin/
│   └── agc_calculation.py       # Algoritma utama QGIS Processing
├── docs/
│   ├── laporan_praktikum.docx   # Laporan praktikum lengkap
│   ├── cara_penggunaan.md       # Panduan penggunaan detail
│   └── banner.png               # Screenshot UI plugin
├── sample_data/
│   └── README.md                # Panduan format data sampel
├── scripts/
│   └── generate_sample_data.py  # Skrip helper buat data dummy
├── LICENSE
└── README.md
```

---

## 📊 Cara Penggunaan

### 1. Siapkan Data

| Data | Format | Keterangan |
|------|--------|-----------|
| Citra Band 4 (Red) | GeoTIFF | Sentinel-2 Level-2A, terkoreksi atmosfer |
| Citra Band 8 (NIR) | GeoTIFF | Proyeksi sama dengan Band 4 |
| Titik Sampel | Shapefile / GeoPackage | Memiliki kolom `AGB` (ton/ha) |

### 2. Jalankan Plugin

1. Buka **Processing Toolbox** → **Analisis Karbon**
2. Klik **Estimasi AGC dari AGB (RF Model)**
3. Isi parameter:

   | Parameter | Keterangan |
   |-----------|-----------|
   | Pilih Band 4 (Red) | Layer raster Band 4 |
   | Pilih Band 8 (NIR) | Layer raster Band 8 |
   | Input Titik Sampel | Layer vektor titik sampel |
   | Nama Field AGB | Nama kolom AGB (default: `AGB`) |
   | Peta Prediksi AGC | Path output GeoTIFF |

4. Klik **Run**
5. Baca laporan di tab **Log**

### 3. Interpretasi Output

```
=============================================
  HASIL ANALISIS STOK KARBON MANGROVE
  Metode: Random Forest | Konversi AGB x 0.47
=============================================
  R²   : 0.8754
  RMSE : 2.3401 Ton C
  MAE  : 1.8920 Ton C
---------------------------------------------
  Total Luas Mangrove : 1250.40 Ha
  Total Stok AGC      : 98750.25 Ton C
  Rata-rata AGC/Ha    : 79.00 Ton C/Ha
=============================================
```

---

## 🧮 Rumus & Metodologi

### NDVI
```
NDVI = (NIR - Red) / (NIR + Red)
```
Nilai berkisar -1 hingga +1. Vegetasi lebat → mendekati 1.

### Konversi AGB ke AGC
```
AGC (Ton C) = AGB (Ton/Ha) × 0.47
```
Faktor 0.47 = fraksi karbon standar IPCC (2006) untuk biomassa tumbuhan tropis.

### Random Forest
- **Algoritma**: `sklearn.ensemble.RandomForestRegressor`
- **n_estimators**: 100 pohon keputusan
- **Pembagian data**: 70% latih / 30% uji
- **Fitur prediktor**: `[Red, NIR, NDVI]`
- **Target**: `AGC (Ton C)`

---

## 📁 Format Data Sampel

File vektor titik sampel harus memiliki minimal satu kolom atribut berisi nilai AGB:

| FID | AGB | Keterangan |
|-----|-----|-----------|
| 1 | 45.2 | Plot mangrove lebat |
| 2 | 28.7 | Plot mangrove sedang |
| 3 | 61.0 | Plot mangrove sangat lebat |

> Satuan AGB: **ton biomassa kering per hektar (ton/ha)**

---

## 📖 Referensi

- IPCC (2006). *Guidelines for National Greenhouse Gas Inventories, Vol. 4*
- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32
- Komiyama, A. et al. (2008). Allometry, biomass, and productivity of mangrove forests. *Aquatic Botany*, 89(2), 128–137
- Rouse, J.W. et al. (1974). Monitoring Vegetation Systems in the Great Plains with ERTS

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detail.

---

## 🤝 Kontribusi

Pull request sangat disambut! Untuk perubahan besar, harap buka issue terlebih dahulu.

1. Fork repository ini
2. Buat branch fitur: `git checkout -b fitur/tambahan-indeks`
3. Commit perubahan: `git commit -m 'Tambah indeks EVI'`
4. Push ke branch: `git push origin fitur/tambahan-indeks`
5. Buka Pull Request

---

<p align="center">
  Dibuat dengan ❤️ untuk pemantauan ekosistem mangrove Indonesia 🇮🇩
</p>
