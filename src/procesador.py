
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

    # ESTADÍSTICAS Y EXPORTACIÓN

    def calcular_estadisticas(self):
        df = self.df

        resumen = df.groupby(["pais", "indicador"])["valor"].agg([
            "mean",
            "max",
            "min"
        ]).reset_index()

        # CRECIMIENTO PIB
        pib = df[df["indicador"].str.contains("PIB", case=False, na=False)].copy()
        pib["crecimiento"] = pib.groupby("pais")["valor"].pct_change() * 100

        # CATEGORIZACIÓN DE INFLACIÓN
        def categorizar(x):
            if x < 3:
                return "Baja"
            elif x < 10:
                return "Moderada"
            else:
                return "Alta"

        mask = df["indicador"].str.contains("Inflaci[oó]n", case=False, na=False)
        df.loc[mask, "categoria_inflacion"] = df.loc[mask, "valor"].apply(categorizar)

        self.df = df
        return resumen

    def exportar_limpio(self, ruta="data/procesado/datos_limpios.csv"):
        self.df.to_csv(ruta, index=False)
        return ruta