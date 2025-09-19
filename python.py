# === 0) Preparación ===
import os
os.makedirs("salidas", exist_ok=True)
print("Working dir:", os.getcwd())
assert os.path.exists("srtm.tif"), "No encuentro srtm.tif en el directorio actual."

# === 1) Librerías ===
# Si te falta matplotlib:  !pip install matplotlib
# Si te falta rasterio:    !pip install rasterio
import numpy as np
import rasterio
import matplotlib.pyplot as plt

# === 2) Cargar DEM y metadatos ===
with rasterio.open("srtm.tif") as src:
    dem = src.read(1).astype("float64")   # banda 1
    profile = src.profile
    transform = src.transform
    nodata = src.nodata

# Manejo simple de NoData (opcional, si existe)
if nodata is not None:
    dem[dem == nodata] = np.nan

# === 3) Calcular gradientes con el tamaño de píxel real ===
xres = transform.a               # tamaño pixel en X (m)
yres = -transform.e              # tamaño pixel en Y (m), transform.e suele ser negativo
gy, gx = np.gradient(dem, yres, xres)  # gradiente por filas (y) y columnas (x)

# === 4) Aspecto en radianes (convención GIS: 0 = Norte, horario) ===
# Fórmula común usando gradientes:
aspect = np.arctan2(gx, -gy)    # resultado en [-pi, pi]
# (opcional) normalizar a [0, 2pi) si lo necesitas:
# aspect = np.where(aspect < 0, aspect + 2*np.pi, aspect)

# === 5) Northness y Eastness ===
northness = np.cos(aspect)
eastness  = np.sin(aspect)

# === 6) Guardar GeoTIFFs ===
out_prof = profile.copy()
out_prof.update(dtype=rasterio.float32, count=1, nodata=None)

with rasterio.open("salidas/northness_python.tif", "w", **out_prof) as dst:
    dst.write(northness.astype(np.float32), 1)

with rasterio.open("salidas/eastness_python.tif", "w", **out_prof) as dst:
    dst.write(eastness.astype(np.float32), 1)

# === 7) Mostrar dentro del notebook ===
plt.figure()
plt.imshow(northness, vmin=-1, vmax=1)
plt.colorbar(label="Northness")
plt.title("Northness (Python)")
plt.show()

plt.figure()
plt.imshow(eastness, vmin=-1, vmax=1)
plt.colorbar(label="Eastness")
plt.title("Eastness (Python)")
plt.show()

# (Opcional) guardar PNG para usarlos en Markdown
plt.imsave("salidas/northness_python.png", northness, vmin=-1, vmax=1)
plt.imsave("salidas/eastness_python.png", eastness, vmin=-1, vmax=1)
