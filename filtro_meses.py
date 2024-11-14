# import csv
# from datetime import datetime
# import os

# # Función para verificar la existencia de la columna "Fecha"
# def verificar_columna_fecha(csv_reader):
#     if "Fecha" not in csv_reader.fieldnames:
#         print("Error: La columna 'Fecha' no existe en el archivo CSV.")
#         return False
#     return True

# # Función para obtener los meses disponibles
# def obtener_meses_disponibles(ruta_csv):
#     meses_disponibles = set()

#     if not os.path.exists(ruta_csv):
#         print(f"Error: El archivo {ruta_csv} no existe.")
#         return meses_disponibles

#     with open(ruta_csv, mode='r') as file:
#         csv_reader = csv.DictReader(file)
        
#         if not verificar_columna_fecha(csv_reader):
#             return meses_disponibles
        
#         for row in csv_reader:
#             try:
#                 fecha = datetime.strptime(row["Fecha"], "%Y-%m-%d %H:%M")
#                 meses_disponibles.add(fecha.month)
#             except ValueError as e:
#                 print(f"Error al convertir la fecha: {e}. Revisa la fila: {row}")

#     return meses_disponibles

# # Función para filtrar por mes
# def filtrar_por_mes(ruta_csv_original, mes):
#     if not os.path.exists(ruta_csv_original):
#         print(f"Error: El archivo {ruta_csv_original} no existe.")
#         return
    
#     nombre_mes = datetime(2000, mes, 1).strftime("%B")
#     ruta_csv_filtrado = f'filtros/filtrado_{nombre_mes}.csv'
#     filas_filtradas = []

#     with open(ruta_csv_original, mode='r') as file:
#         csv_reader = csv.DictReader(file)

#         if not verificar_columna_fecha(csv_reader):
#             return
        
#         for row in csv_reader:
#             try:
#                 fecha = datetime.strptime(row["Fecha"], "%Y-%m-%d %H:%M")
#                 if fecha.month == mes:
#                     filas_filtradas.append(row)
#             except ValueError as e:
#                 print(f"Error al convertir la fecha: {e}. Revisa la fila: {row}")

#     if filas_filtradas:
#         os.makedirs("filtros", exist_ok=True)
#         with open(ruta_csv_filtrado, mode='w', newline='') as file:
#             csv_writer = csv.DictWriter(file, fieldnames=csv_reader.fieldnames)
#             csv_writer.writeheader()
#             csv_writer.writerows(filas_filtradas)
#         print(f"CSV filtrado guardado en: {ruta_csv_filtrado}")
#     else:
#         print(f"No se encontraron filas para el mes {mes}.")

# # Función principal
# def main():
#     ruta_csv = '2024.csv'

#     meses_disponibles = obtener_meses_disponibles(ruta_csv)

#     if not meses_disponibles:
#         print("No se encontraron meses disponibles en el archivo CSV.")
#         return

#     for mes in sorted(meses_disponibles):
#         filtrar_por_mes(ruta_csv, mes)

# if __name__ == "__main__":
#     main()

import csv
from datetime import datetime
import os

RUTA_FILTROS = "filtros"
FORMATO_FECHA = "%Y-%m-%d %H:%M"
COLUMNA_FECHA = "Fecha"

# Función para verificar la existencia de la columna "Fecha"
def verificar_columna_fecha(csv_reader):
    if COLUMNA_FECHA not in csv_reader.fieldnames:
        print(f"Error: La columna '{COLUMNA_FECHA}' no existe en el archivo CSV.")
        return False
    return True

# Función para obtener los meses disponibles
def obtener_meses_disponibles(ruta_csv):
    meses_disponibles = set()

    if not os.path.exists(ruta_csv):
        print(f"Error: El archivo '{ruta_csv}' no existe.")
        return meses_disponibles

    with open(ruta_csv, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        if not verificar_columna_fecha(csv_reader):
            return meses_disponibles
        
        for row in csv_reader:
            try:
                fecha = datetime.strptime(row[COLUMNA_FECHA], FORMATO_FECHA)
                meses_disponibles.add(fecha.month)
            except ValueError as e:
                print(f"Error al convertir la fecha en la fila {row}: {e}")

    return meses_disponibles

# Función para filtrar por mes y guardar en archivo
def filtrar_por_mes(ruta_csv_original, mes):
    if not os.path.exists(ruta_csv_original):
        print(f"Error: El archivo '{ruta_csv_original}' no existe.")
        return
    
    nombre_mes = datetime(2000, mes, 1).strftime("%B")
    ruta_csv_filtrado = os.path.join(RUTA_FILTROS, f'filtrado_{nombre_mes}.csv')
    filas_filtradas = []

    with open(ruta_csv_original, mode='r') as file:
        csv_reader = csv.DictReader(file)

        if not verificar_columna_fecha(csv_reader):
            return
        
        for row in csv_reader:
            try:
                fecha = datetime.strptime(row[COLUMNA_FECHA], FORMATO_FECHA)
                if fecha.month == mes:
                    filas_filtradas.append(row)
            except ValueError as e:
                print(f"Error al convertir la fecha en la fila {row}: {e}")

    if filas_filtradas:
        os.makedirs(RUTA_FILTROS, exist_ok=True)
        with open(ruta_csv_filtrado, mode='w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=csv_reader.fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(filas_filtradas)
        print(f"CSV filtrado guardado en: {ruta_csv_filtrado}")
    else:
        print(f"No se encontraron filas para el mes {mes}.")

# Función principal
def main():
    ruta_csv = '2024.csv'

    meses_disponibles = obtener_meses_disponibles(ruta_csv)

    if not meses_disponibles:
        print("No se encontraron meses disponibles en el archivo CSV.")
        return

    for mes in sorted(meses_disponibles):
        filtrar_por_mes(ruta_csv, mes)

if __name__ == "__main__":
    main()
