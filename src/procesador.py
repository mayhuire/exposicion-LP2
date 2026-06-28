
import pandas as pd
import re

# PROCESADOR DE DATOS 

class ProcesadorEconomico:

    def __init__(self):
        self.df = pd.DataFrame()

    def cargar_datos(self, ruta_json):
        return pd.read_json(ruta_json)

    def unir_datasets(self, lista_df):
        self.df = pd.concat(lista_df, ignore_index=True)
        return self.df
    
# LIMPIEZA Y REGEX

def limpiar_y_transformar(self):

    df = self.df.copy()

    df["anio"] = df["fecha_original"].astype(str).str.extract(r"(\d{4})")
    df["anio"] = df["anio"].astype(int)

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["valor"])

    df = df.sort_values(by=["pais", "indicador", "anio"])

    self.df = df
    return df
