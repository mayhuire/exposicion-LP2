# config.py
# Configuración central del proyecto ANALATAM

# Países a analizar
PAISES = {
    "Perú": "PER",
    "Chile": "CHL",
    "Colombia": "COL",
    "México": "MEX",
    "Brasil": "BRA"
}

# Indicadores económicos del Banco Mundial
INDICADORES = {
    "PIB_per_capita_USD": "NY.GDP.PCAP.CD",
    "Inflacion_IPC_anual": "FP.CPI.TOTL.ZG",
    "Desempleo_total": "SL.UEM.TOTL.ZS"
}

# Período de análisis
ANIO_INICIO = 2000
ANIO_FIN = 2023

# Rutas de carpetas (relativas a la raíz del proyecto)
CARPETA_CRUDO = "data/crudo"
CARPETA_PROCESADO = "data/procesado"
ARCHIVO_PROCESADO = "data/procesado/datos_limpios.csv"
CARPETA_OUTPUT = "output"