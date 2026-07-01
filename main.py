# main.py
# Orquestador del proyecto – Ejecuta el flujo completo

import os
import shutil
from config import PAISES, INDICADORES, ANIO_INICIO, ANIO_FIN, CARPETA_CRUDO, ARCHIVO_PROCESADO, CARPETA_OUTPUT
from src.api_economia import APIEconomia
from src.procesador import ProcesadorEconomico
from src.visualizador import VisualizadorEconomico


def paso1_obtener_datos():
    print("\n===== PASO 1: OBTENIENDO DATOS DE LA API =====")
    api = APIEconomia()
    usar_respaldo = False

    for nombre_pais, cod_pais in PAISES.items():
        for nombre_indicador, cod_indicador in INDICADORES.items():
            print(f"Consultando {nombre_indicador} para {nombre_pais}...")
            try:
                datos = api.obtener_datos(cod_pais, cod_indicador, ANIO_INICIO, ANIO_FIN)
                nombre_archivo = f"{cod_pais}_{cod_indicador.replace('.', '_')}.json"
                api.guardar_json(datos, nombre_archivo)
            except Exception as e:
                print(f"  ⚠ Error: {e}")
                usar_respaldo = True
                break
        if usar_respaldo:
            break

    if usar_respaldo:
        print("\nLa API no responde. Se usará el archivo de respaldo local 'datos_respaldo.json'.")
        ruta_respaldo = os.path.join(CARPETA_CRUDO, "datos_respaldo.json")
        if not os.path.exists(ruta_respaldo):
            print("ERROR: No se encontró el archivo de respaldo. Asegúrate de crearlo en data/crudo/")
            return
        # Copiar el respaldo como un archivo por cada combinación (para mantener la lógica del procesador)
        for nombre_pais, cod_pais in PAISES.items():
            for nombre_indicador, cod_indicador in INDICADORES.items():
                nombre_archivo = f"{cod_pais}_{cod_indicador.replace('.', '_')}.json"
                ruta_destino = os.path.join(CARPETA_CRUDO, nombre_archivo)
                shutil.copy(ruta_respaldo, ruta_destino)
        print("Archivos de respaldo generados.\n")
    else:
        print("Paso 1 completado.\n")


def paso2_procesar_datos():
    """Paso 2: Cargar JSON crudos, limpiar, transformar y exportar CSV."""
    print("\n===== PASO 2: PROCESANDO DATOS =====")
    proc = ProcesadorEconomico()

    # Cargar todos los archivos JSON de la carpeta crudo
    lista_df = []
    for archivo in os.listdir(CARPETA_CRUDO):
        if archivo.endswith(".json"):
            ruta = os.path.join(CARPETA_CRUDO, archivo)
            try:
                df_temp = proc.cargar_datos(ruta)
                lista_df.append(df_temp)
            except Exception as e:
                print(f"  ⚠ Error al cargar {archivo}: {e}")

    if not lista_df:
        raise FileNotFoundError("No se encontraron archivos JSON para procesar. Verifica el paso 1.")

    # Unir en un solo DataFrame
    proc.unir_datasets(lista_df)
    print(f"Registros antes de limpieza: {len(proc.df)}")

    # Limpiar y transformar
    proc.limpiar_y_transformar()
    print(f"Registros después de limpieza: {len(proc.df)}")

    # Calcular estadísticas e imprimir resumen
    resumen = proc.calcular_estadisticas()
    print("\nResumen estadístico por país e indicador:")
    print(resumen.to_string(index=False))

    # Exportar CSV limpio
    ruta_csv = proc.exportar_limpio(ARCHIVO_PROCESADO)
    print(f"\nDatos limpios exportados a: {ruta_csv}")
    print("Paso 2 completado.\n")


def paso3_visualizar():
    """Paso 3: Generar los gráficos a partir del CSV procesado."""
    print("\n===== PASO 3: GENERANDO GRÁFICOS =====")
    viz = VisualizadorEconomico(ARCHIVO_PROCESADO, CARPETA_OUTPUT)
    viz.cargar_datos()

    # 1. Gráfico de líneas: evolución del PIB per cápita en Perú
    print("Generando gráfico de líneas...")
    try:
        ruta_lineas = viz.grafico_lineas("Perú", "PIB", ANIO_INICIO, ANIO_FIN)
        print(f"  ✓ {ruta_lineas}")
    except Exception as e:
        print(f"  ⚠ {e}")

    # 2. Gráfico de barras: comparativa de inflación promedio en 2023
    print("Generando gráfico de barras...")
    try:
        ruta_barras = viz.grafico_barras("Inflación", 2023)
        print(f"  ✓ {ruta_barras}")
    except Exception as e:
        print(f"  ⚠ {e}")

    # 3. Gráfico de dispersión: relación desempleo vs inflación en 2023
    print("Generando gráfico de dispersión...")
    try:
        ruta_disp = viz.grafico_dispersion("Desempleo", "Inflación", 2023)
        print(f"  ✓ {ruta_disp}")
    except Exception as e:
        print(f"  ⚠ {e}")

    # 4. (Opcional) Gráfico de pastel de categorías de inflación
    print("Generando gráfico de pastel (categorías de inflación)...")
    try:
        ruta_pastel = viz.grafico_pastel(2023)
        if ruta_pastel:
            print(f"  ✓ {ruta_pastel}")
        else:
            print("  - No se generó (posible falta de columna 'categoria_inflacion')")
    except Exception as e:
        print(f"  ⚠ {e}")

    print("Paso 3 completado.\n")


if __name__ == "__main__":
    # Crear carpetas necesarias si no existen
    os.makedirs(CARPETA_CRUDO, exist_ok=True)
    os.makedirs("data/procesado", exist_ok=True)
    os.makedirs(CARPETA_OUTPUT, exist_ok=True)

    # Ejecutar el flujo
    paso1_obtener_datos()
    paso2_procesar_datos()
    paso3_visualizar()

    print("\n===== PROYECTO COMPLETADO EXITOSAMENTE =====")
    print("Revisa las carpetas 'data/crudo', 'data/procesado' y 'output'.")