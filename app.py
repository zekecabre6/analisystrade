#app.py
from flask import Flask, jsonify, request, send_file
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones CORS desde el frontend

RUTA_FILTROS = "filtros"  # Ruta a la carpeta que contiene los CSVs
RUTA_RESULTADOS = "resultados"
EQUIVALENCIAS_RESULTADOS = {
    "ganadas": ["ganada", "ganadas"],
    "perdidas": ["perdida", "perdidas"],
    "empate": ["break even", "break-even","empate"],
    "preventiva": ["cierre preventivo", "Cierre Preventivo"]
}

def cargar_resultados(ruta_csv):
    """Consolidar resultados de operaciones desde el archivo CSV"""
    if not os.path.exists(ruta_csv):
        return None

    resultados = {clave: 0 for clave in EQUIVALENCIAS_RESULTADOS}
    with open(ruta_csv, mode='r') as file:
        csv_reader = csv.DictReader(file)
        if "Resultado" not in csv_reader.fieldnames:
            return None
        for row in csv_reader:
            tipo = row["Resultado"].strip().lower()
            for clave, variaciones in EQUIVALENCIAS_RESULTADOS.items():
                if tipo in variaciones:
                    resultados[clave] += 1
                    break
    return resultados

def calcular_estadisticas_moneda(df):
    """Calcular estadísticas por moneda"""
    estadisticas = {}
    df["Porcentaje 24hs"] = pd.to_numeric(df["Porcentaje 24hs"], errors="coerce")

    for moneda, grupo in df.groupby("Nombre"):
        estadisticas[moneda] = {
            "rendimiento_promedio": grupo["Porcentaje 24hs"].mean()
        }
        for col in ["Precio", "Precio Esperado", "Menor precio", "Mayor precio", "Stop Loss"]:
            if col in grupo.columns:
                estadisticas[moneda][f"{col}_promedio"] = grupo[col].mean()
                estadisticas[moneda][f"{col}_desviacion"] = grupo[col].std()

        if {"Fecha", "Fecha Completado"}.issubset(grupo.columns):
            grupo["Fecha"] = pd.to_datetime(grupo["Fecha"], errors='coerce')
            grupo["Fecha Completado"] = pd.to_datetime(grupo["Fecha Completado"], errors='coerce')
            grupo["Duracion"] = (grupo["Fecha Completado"] - grupo["Fecha"]).dt.total_seconds() / 3600
            estadisticas[moneda]["duracion_promedio"] = grupo["Duracion"].mean()

    return estadisticas

def crear_graficos(resultados, estadisticas_por_moneda, mes_nombre):
    """Crear y devolver gráficos en memoria"""
    rutas_graficos = []

    # Gráfico de resultados por tipo (barras)
    plt.bar(resultados.keys(), resultados.values(), color=['green', 'red', 'blue', 'orange'])
    plt.xlabel('Tipo de Resultado')
    plt.ylabel('Cantidad')
    plt.title(f'Resultados de Operaciones - {mes_nombre}')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    rutas_graficos.append(img)
    plt.close()

    # Gráfico de rendimiento promedio por moneda (barras)
    plt.bar(estadisticas_por_moneda.keys(),
            [moneda["rendimiento_promedio"] for moneda in estadisticas_por_moneda.values()],
            color='purple')
    plt.xlabel('Moneda')
    plt.ylabel('Rendimiento Promedio (%)')
    plt.title(f'Rendimiento Promedio por Moneda - {mes_nombre}')
    plt.xticks(rotation=45)
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    rutas_graficos.append(img)
    plt.close()

    # Gráfico de pastel de resultados
    plt.pie(resultados.values(), labels=resultados.keys(), autopct='%1.1f%%', 
            colors=['green', 'red', 'blue', 'orange'])
    plt.title(f'Distribución de Resultados - {mes_nombre}')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    rutas_graficos.append(img)
    plt.close()

    return rutas_graficos

@app.route('/archivos', methods=['GET'])
def obtener_archivos():
    archivos_csv = [f for f in os.listdir(RUTA_FILTROS) if f.endswith('.csv')]
    return jsonify(archivos_csv)

@app.route('/resultados', methods=['GET'])
def obtener_resultados():
    archivo = request.args.get('archivo')  # Obtener el nombre del archivo desde la query string
    if not archivo:
        return jsonify({"error": "No se proporcionó un archivo"}), 400

    ruta_csv = os.path.join(RUTA_FILTROS, archivo)  # Ruta completa al archivo CSV
    resultados = cargar_resultados(ruta_csv)
    
    if resultados:
        return jsonify(resultados)
    else:
        return jsonify({"error": "No se pudieron cargar los resultados."}), 500

@app.route('/informe', methods=['GET'])
def generar_informe_api():
    archivo = request.args.get('archivo')
    if not archivo:
        return jsonify({"error": "No se proporcionó un archivo"}), 400

    ruta_csv = os.path.join(RUTA_FILTROS, archivo)
    if not os.path.exists(ruta_csv):
        return jsonify({"error": f"El archivo {archivo} no existe."}), 404

    try:
        df = pd.read_csv(ruta_csv)
        resultados = cargar_resultados(ruta_csv)
        
        if resultados:
            estadisticas_por_moneda = calcular_estadisticas_moneda(df)
            mes_nombre = archivo.split('_')[1]  # Suponiendo que el nombre del archivo contiene el mes
            rutas_graficos = crear_graficos(resultados, estadisticas_por_moneda, mes_nombre)
            
            # Devolver los gráficos como imágenes
            return send_file(rutas_graficos[0], mimetype='image/png', as_attachment=True, download_name=f'grafico_resultados_{mes_nombre}.png')
        
        return jsonify({"error": "No se pudo generar el informe debido a errores en el archivo CSV."}), 500
    
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
