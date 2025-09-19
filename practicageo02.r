# === 0) Carpeta y verificación de ruta de trabajo ===
dir.create("salidas", showWarnings = FALSE)
getwd()  # verifica que aquí está tu srtm.tif

# === 1) Librerías ===
if (!require(terra)) install.packages("terra"); library(terra)

# === 2) Cargar DEM (asegúrate de que el archivo está en este directorio) ===
# Si tu archivo se llama diferente, cambia "srtm.tif"
stopifnot(file.exists("srtm.tif"))
dem <- rast("srtm.tif")

# === 3) Calcular aspecto en radianes ===
aspect <- terrain(dem, v = "aspect", unit = "radians")  # NA en zonas planas está bien

# === 4) Calcular Northness y Eastness ===
northness <- cos(aspect)
eastness  <- sin(aspect)

# === 5) Guardar salidas GeoTIFF ===
writeRaster(northness, "salidas/northness_R.tif", overwrite = TRUE)
writeRaster(eastness,  "salidas/eastness_R.tif",  overwrite = TRUE)

# === 6) Mostrar dentro del notebook ===
plot(northness, main = "Northness (R)  cos(aspect)")
plot(eastness,  main = "Eastness (R)  sin(aspect)")

# (Opcional) Guardar PNG para usarlos en celdas Markdown
png("salidas/northness_R.png", width = 1200, height = 900, res = 150)
plot(northness, main = "Northness (R)")
dev.off()

png("salidas/eastness_R.png", width = 1200, height = 900, res = 150)
plot(eastness, main = "Eastness (R)")
dev.off()
