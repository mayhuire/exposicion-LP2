import requests
import json
import os
import re


class APIEconomia:

    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"

    def obtener_datos(self, pais, indicador, anio_inicio=2000, anio_fin=2023):
        """
        Obtiene los datos desde la API del Banco Mundial.
        """

        url = (
            f"{self.base_url}/country/{pais}/indicator/{indicador}"
            f"?format=json&date={anio_inicio}:{anio_fin}&per_page=100"
        )

        try:
            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status()
            datos_json = respuesta.json()

            lista_datos = []

            for dato in datos_json[1]:
                lista_datos.append({
                    "pais": dato["country"]["value"],
                    "indicador": dato["indicator"]["value"],
                    "anio": dato["date"],
                    "valor": dato["value"]
                })

            return lista_datos

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al conectar con la API: {e}")