---

# 🌿 Karbon Mangrove QGIS — AGC Estimation Plugin

## 📋 Description

A QGIS Toolbox based on the *Python Processing Framework* for estimating *Above Ground Carbon (AGC)* in mangrove ecosystems using the *Random Forest Regressor* algorithm.

<img width="599" height="629" alt="image" src="https://github.com/user-attachments/assets/651424f7-fe3b-421d-9893-d5f3732662b9" />


<p align="center">
  <img src="https://img.shields.io/badge/QGIS-3.x-green?logo=qgis&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-RandomForest-orange"/>
  <img src="https://img.shields.io/badge/Sentinel--2-Band%204%20%26%208-lightblue"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow"/>
</p>

---

This toolbox integrates *Sentinel-2* spectral image data (Band 4/Red & Band 8/NIR) with field sample data of *Above Ground Biomass (AGB)* to produce spatial carbon stock prediction maps.


---

## Main Workflow

```text
  Sentinel-2 Image          Field Sample Points
  Band 4 (Red)    +       AGB (ton/ha)
  Band 8 (NIR)                │
        │                     │
        └────────┬────────────┘
                 │
        Pixel Extraction
        (native:rastersampling)
                 │
        Calculate NDVI + AGC Conversion
        AGC = AGB × 0.47 (IPCC)
                 │
        Random Forest Training
        (n_estimators=100, test_size=30%)
                 │
        Full-Extent Raster Prediction
                 │
        ┌────────┴────────────┐
   AGC Map (GeoTIFF)    Statistical Report
   (Ton C / pixel)      (R², RMSE, Total C)

```

---

## 🚀 Features

* ✅ **Flexible Input** — Supports all GDAL raster & OGR vector formats
* ✅ **Automatic NDVI** — Calculated directly from Red & NIR Bands
* ✅ **Standard IPCC AGC Conversion** — 0.47 conversion factor following international guidelines
* ✅ **Model Evaluation** — R², RMSE, and MAE reported directly in QGIS logs
* ✅ **Row-by-Row Prediction** — Efficient for large-scale rasters
* ✅ **GeoTIFF Float32 Output** — Compatible with all major GIS software
* ✅ **Carbon Statistical Report** — Total area, total AGC, and average AGC/Ha

---

## 📦 Installation

### Prerequisites

| Component | Version |
| --- | --- |
| QGIS | ≥ 3.16 |
| Python | ≥ 3.9 |
| scikit-learn | ≥ 1.0 |
| numpy | ≥ 1.21 |
| GDAL/OGR | ≥ 3.3 |

### Installing scikit-learn in OSGeo4W (Windows)

Open **OSGeo4W Shell** as Administrator and run:

```bash
python -m pip install scikit-learn

```

### Plugin Installation

1. Download or clone this repository:
```bash
git clone https://github.com/rosyidpaundra/karbon-mangrove-qgis.git

```


2. Copy the `plugin/` folder into your QGIS Processing Scripts directory:
* **Windows:** `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts\`
* **Linux/Mac:** `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts/`


3. Open QGIS → **Processing Toolbox** → Refresh Scripts.
4. The plugin will appear under: **Carbon Analysis → AGC Estimation from AGB (RF Model)**.

---

## 🗂️ Repository Structure

```text
karbon-mangrove-qgis/
├── plugin/
│   └── agc_calculation.py       # Main QGIS Processing algorithm
├── docs/
│   ├── usage_guide.md           # Detailed user guide
│   └── banner.png               # Plugin UI screenshot
├── sample_data/
│   └── README.md                # Sample data format guide
├── scripts/
│   └── generate_sample_data.py  # Helper script to create dummy data
├── LICENSE
└── README.md

```

---

## 📊 How to Use

### 1. Prepare Data

| Data | Format | Description |
| --- | --- | --- |
| Band 4 (Red) Image | GeoTIFF | Sentinel-2 Level-2A, atmospherically corrected |
| Band 8 (NIR) Image | GeoTIFF | Same projection as Band 4 |
| Sample Points | Shapefile / GeoPackage | Must contain an AGB field (ton/ha) |

### 2. Run the Plugin

1. Open **Processing Toolbox** → **Carbon Analysis**.
2. Click **AGC Estimation from AGB (RF Model)**.
3. Fill in the parameters:
| Parameter | Description |
| --- | --- |
| Select Band 4 (Red) | Band 4 raster layer |
| Select Band 8 (NIR) | Band 8 raster layer |
| Input Sample Points | Point sample vector layer |
| AGB Field Name | Column name for AGB (default: `AGB`) |
| AGC Prediction Map | Output GeoTIFF file path |


4. Click **Run**.
5. View the summary report in the **Log** tab.

### 3. Output Interpretation

```text
=============================================
      MANGROVE CARBON STOCK ANALYSIS RESULTS
   Method: Random Forest | Conversion: AGB x 0.47
=============================================
  R²   : 0.8754
  RMSE : 2.3401 Ton C
  MAE  : 1.8920 Ton C
---------------------------------------------
  Total Mangrove Area : 1250.40 Ha
  Total AGC Stock     : 98750.25 Ton C
  Average AGC/Ha      : 79.00 Ton C/Ha
=============================================

```

---

## 🧮 Formulas & Methodology

### NDVI

$$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$


Values range from -1 to +1. Dense vegetation approaches +1.

### AGB to AGC Conversion

$$\text{AGC (Ton C)} = \text{AGB (Ton/Ha)} \times 0.47$$


The $0.47$ factor is the IPCC (2006) standard carbon fraction for tropical plant biomass.

### Random Forest

* **Algorithm:** `sklearn.ensemble.RandomForestRegressor`
* **n_estimators:** 100 decision trees
* **Data Split:** 70% training / 30% testing
* **Predictor Features:** `[Red, NIR, NDVI]`
* **Target Variable:** `AGC (Ton C)`

---

## 📁 Sample Data Format

The vector layer file containing sample points must have at least one attribute column for AGB values:

| FID | AGB | Description |
| --- | --- | --- |
| 1 | 45.2 | Dense mangrove plot |
| 2 | 28.7 | Moderate mangrove plot |
| 3 | 61.0 | Very dense mangrove plot |

*AGB Unit: dry biomass tons per hectare (ton/ha).*

---

## 📖 References

* IPCC (2006). *Guidelines for National Greenhouse Gas Inventories, Vol. 4*.
* Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.
* Komiyama, A. et al. (2008). Allometry, biomass, and productivity of mangrove forests. *Aquatic Botany*, 89(2), 128–137.
* Rouse, J.W. et al. (1974). Monitoring Vegetation Systems in the Great Plains with ERTS.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](https://github.com/rosyidpaundra/karbon-mangrove-qgis/blob/main/LICENSE) file for details.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork this repository
2. Create your feature branch: `git checkout -b feature/add-index`
3. Commit your changes: `git commit -m 'Add EVI index'`
4. Push to the branch: `git push origin feature/add-index`
5. Open a Pull Request

---

*Made with ❤️ for monitoring Indonesia's mangrove ecosystems 🇮🇩*
