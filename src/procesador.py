
import pandas as pd
import re

# PROCESADOR DE DATOS 

class ProcesadorEconomico:

    def __init__(self):
# 		DataFrame principal donde se almacenarán los datos procesados
        self.df = pd.DataFrame()

    def cargar_datos(self, ruta_json):
#       Carga un archivo JSON y devuelve un DataFrame.
        return pd.read_json(ruta_json)

    def unir_datasets(self, lista_df):
#       Concatena una lista de DataFrames en uno solo y lo guarda en self.df.
        self.df = pd.concat(lista_df, ignore_index=True)
        return self.df
    

    # LIMPIEZA Y REGEX

    def limpiar_y_transformar(self):
        df = self.df.copy()
        
        # Extraer año (4 dígitos) de la columna 'fecha_original'
        df["anio"] = df["fecha_original"].astype(str).str.extract(r"(\d{4})")
        df["anio"] = df["anio"].astype(int)

        # Convertir la columna 'valor' a numérico, forzando errores a NaN
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        # Eliminar filas donde 'valor' sea NaN
        df = df.dropna(subset=["valor"])
        
        # Ordenar por país, indicador y año para facilitar análisis posteriores
        df = df.sort_values(by=["pais", "indicador", "anio"])

        self.df = df
        return df

    # ESTADÍSTICAS Y EXPORTACIÓN

    def calcular_estadisticas(self):
        df = self.df

        # Resumen estadístico agrupado
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

        # Aplicar la categorización solo a los indicadores que contengan "Inflación" o "Inflación"
        mask = df["indicador"].str.contains("Inflaci[oó]n", case=False, na=False)
        df.loc[mask, "categoria_inflacion"] = df.loc[mask, "valor"].apply(categorizar)

        self.df = df
        return resumen

    def exportar_limpio(self, ruta="data/procesado/datos_limpios.csv"):
        self.df.to_csv(ruta, index=False)
        return ruta