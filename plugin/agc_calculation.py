from typing import Any, Optional
import numpy as np
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterString,
)
from qgis import processing

try:
    from osgeo import gdal
except ImportError:
    import gdal

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
except ImportError:
    raise QgsProcessingException("Library 'scikit-learn' belum terinstall di OSGeo4W.")


class AGCCalculationAlgorithm(QgsProcessingAlgorithm):
    """
    Algoritma QGIS Processing untuk estimasi Above Ground Carbon (AGC)
    pada ekosistem mangrove menggunakan Random Forest Regressor.

    Input:
      - Band 4 (Red) citra Sentinel-2
      - Band 8 (NIR) citra Sentinel-2
      - Titik sampel lapangan dengan atribut AGB (ton/ha)

    Output:
      - Raster prediksi AGC (Ton C) dalam format GeoTIFF Float32
    """

    RED_BAND    = "RED_BAND"
    NIR_BAND    = "NIR_BAND"
    INPUT_VEKTOR = "INPUT_VEKTOR"
    FIELD_AGB   = "FIELD_AGB"
    OUTPUT_RASTER = "OUTPUT_RASTER"

    def name(self) -> str:
        return "agc_from_agb_model"

    def displayName(self) -> str:
        return "Estimasi AGC dari AGB (RF Model)"

    def group(self) -> str:
        return "Analisis Karbon"

    def createInstance(self):
        return AGCCalculationAlgorithm()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer(self.RED_BAND, "Pilih Band 4 (Red)"))
        self.addParameter(QgsProcessingParameterRasterLayer(self.NIR_BAND, "Pilih Band 8 (NIR)"))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_VEKTOR,
            "Input Titik Sampel (Vector)",
            [QgsProcessing.SourceType.TypeVectorPoint]
        ))

        self.addParameter(QgsProcessingParameterString(
            self.FIELD_AGB,
            "Nama Field AGB di Data Vektor",
            defaultValue="AGB"
        ))

        self.addParameter(QgsProcessingParameterRasterDestination(
            self.OUTPUT_RASTER,
            "Peta Prediksi AGC (Ton C)"
        ))

    def processAlgorithm(self, parameters, context, feedback):
        # ── 1. Resolusi Parameter ──────────────────────────────────────────────
        red_layer = self.parameterAsRasterLayer(parameters, self.RED_BAND, context)
        nir_layer = self.parameterAsRasterLayer(parameters, self.NIR_BAND, context)
        agb_field = self.parameterAsString(parameters, self.FIELD_AGB, context)

        # ── 2. Ekstraksi Nilai Piksel ──────────────────────────────────────────
        feedback.pushInfo("Mengekstraksi nilai piksel (B4 & B8)...")

        sampled_red = processing.run("native:rastersampling", {
            'INPUT':       parameters[self.INPUT_VEKTOR],
            'RASTERCOPY':  parameters[self.RED_BAND],
            'COLUMN_PREFIX': 'RED_',
            'OUTPUT':      'memory:sampled_red'
        }, context=context, feedback=feedback)['OUTPUT']

        sampled_all = processing.run("native:rastersampling", {
            'INPUT':       sampled_red,
            'RASTERCOPY':  parameters[self.NIR_BAND],
            'COLUMN_PREFIX': 'NIR_',
            'OUTPUT':      'memory:sampled_all'
        }, context=context, feedback=feedback)['OUTPUT']

        # ── 3. Konstruksi Fitur & Konversi AGB → AGC ──────────────────────────
        X, y = [], []
        for f in sampled_all.getFeatures():
            attrs    = f.attributes()
            val_red  = attrs[-2]
            val_nir  = attrs[-1]
            val_agb  = f[agb_field]

            if None not in [val_red, val_nir, val_agb]:
                red, nir = float(val_red), float(val_nir)
                ndvi = (nir - red) / (nir + red) if (nir + red) != 0 else 0

                # Konversi AGB → AGC menggunakan faktor IPCC 0.47
                val_agc = float(val_agb) * 0.47

                X.append([red, nir, ndvi])
                y.append(val_agc)

        X, y = np.array(X), np.array(y)

        if len(y) < 5:
            raise QgsProcessingException(
                f"Sampel terlalu sedikit ({len(y)} titik valid). "
                "Minimal diperlukan 5 titik sampel."
            )

        # ── 4. Training & Evaluasi Random Forest ──────────────────────────────
        feedback.pushInfo(f"Training RF dengan {len(y)} sampel...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)

        y_pred   = rf.predict(X_test)
        rmse     = np.sqrt(mean_squared_error(y_test, y_pred))
        mae      = mean_absolute_error(y_test, y_pred)
        r2       = r2_score(y_test, y_pred)

        # ── 5. Prediksi Raster Row-by-Row ─────────────────────────────────────
        ds_red       = gdal.Open(red_layer.source())
        ds_nir       = gdal.Open(nir_layer.source())
        rows, cols   = ds_red.RasterYSize, ds_red.RasterXSize
        geotransform = ds_red.GetGeoTransform()
        pixel_area_ha = (abs(geotransform[1]) * abs(geotransform[5])) / 10000

        output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        driver  = gdal.GetDriverByName('GTiff')
        out_ds  = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
        out_ds.SetGeoTransform(geotransform)
        out_ds.SetProjection(ds_red.GetProjection())

        total_agc_ton = 0.0
        total_area_ha = 0.0

        feedback.pushInfo("Memprediksi raster AGC...")
        for r in range(rows):
            if feedback.isCanceled():
                break

            red_row = ds_red.GetRasterBand(1).ReadAsArray(0, r, cols, 1).ravel().astype(float)
            nir_row = ds_nir.GetRasterBand(1).ReadAsArray(0, r, cols, 1).ravel().astype(float)

            with np.errstate(divide='ignore', invalid='ignore'):
                ndvi_row = np.nan_to_num((nir_row - red_row) / (nir_row + red_row))

            row_X    = np.nan_to_num(np.stack([red_row, nir_row, ndvi_row], axis=1))
            row_pred = rf.predict(row_X)

            mask = row_pred > 0
            total_agc_ton += np.sum(row_pred[mask])
            total_area_ha += np.count_nonzero(mask) * pixel_area_ha

            out_ds.GetRasterBand(1).WriteArray(row_pred.reshape(1, cols), 0, r)
            feedback.setProgress(int((r / rows) * 100))

        # ── 6. Laporan ────────────────────────────────────────────────────────
        feedback.pushInfo("\n" + "=" * 45)
        feedback.pushInfo("  HASIL ANALISIS STOK KARBON MANGROVE")
        feedback.pushInfo("  Metode: Random Forest | Konversi AGB x 0.47")
        feedback.pushInfo("=" * 45)
        feedback.pushInfo(f"  R²   : {r2:.4f}")
        feedback.pushInfo(f"  RMSE : {rmse:.4f} Ton C")
        feedback.pushInfo(f"  MAE  : {mae:.4f} Ton C")
        feedback.pushInfo("-" * 45)
        feedback.pushInfo(f"  Total Luas Mangrove : {total_area_ha:.2f} Ha")
        feedback.pushInfo(f"  Total Stok AGC      : {total_agc_ton:.2f} Ton C")
        avg = total_agc_ton / total_area_ha if total_area_ha > 0 else 0
        feedback.pushInfo(f"  Rata-rata AGC/Ha    : {avg:.2f} Ton C/Ha")
        feedback.pushInfo("=" * 45 + "\n")

        out_ds.FlushCache()
        out_ds = None
        return {self.OUTPUT_RASTER: output_path}
