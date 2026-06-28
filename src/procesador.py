
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
    
