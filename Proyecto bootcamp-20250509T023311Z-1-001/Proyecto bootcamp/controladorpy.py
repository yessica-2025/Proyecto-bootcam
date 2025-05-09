import os
import io
import json
import matplotlib
import pandas as pd
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import matplotlib.pyplot as plt
matplotlib.use('Agg') 

app = Flask(__name__)
CORS(app)

csv_file = '06 hydro-share-energy.csv'
json_file = 'datos_hidro.json'
energia=[]

# Función para leer datos desde el archivo JSON
def lee_datos():
    if os.path.exists(json_file):
        with open(json_file, "r") as txt:
            return json.load(txt)
    else:
        return []

# Verificar si el archivo CSV existe y convertirlo en JSON si no existe el archivo JSON
if not os.path.exists(csv_file):
    print(f"El archivo {csv_file} no existe. No se pueden cargar los datos desde CSV.")
    datos_hidro = []
else:
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=["Code"])  # Eliminar filas con valores faltantes en la columna 'Code'
    
    # Convertir el DataFrame a una lista de diccionarios
    datos_hidro = df.to_dict(orient='records')

    # Guardar los datos en el archivo JSON
    with open(json_file, "w") as json_out:
        json.dump(datos_hidro, json_out, indent=4)

    print(f"Datos guardados correctamente en {json_file}")

@app.route('/hidro', methods=["GET"])
def get_hidro():
    # Leer los datos desde el archivo JSON
    datos_hidro = lee_datos()
    return jsonify(datos_hidro)

@app.route('/insertar', methods=["POST"])
def insertar():
    # Obtener los datos JSON enviados en la solicitud
    datos = request.json
    
    # Validar que los datos contienen los campos necesarios (por ejemplo, 'Entity', 'Year', etc.)
    required_fields = ['Entity', 'Year', 'Hydro (% equivalent primary energy)']
    if not all(field in datos for field in required_fields):
        return jsonify({"message": "Datos incompletos. Asegúrate de que todos los campos requeridos estén presentes."}), 400
    
    # Leer los datos actuales desde el archivo JSON
    datos_hidro = lee_datos()
    
    # Agregar el nuevo dato al final de la lista de datos
    datos_hidro.append(datos)
    
    # Escribir los datos actualizados en el archivo JSON
    with open(json_file, "w") as json_out:
        json.dump(datos_hidro, json_out, indent=4)
    
    # Devolver una respuesta de éxito con el dato insertado
    return jsonify({"message": "Dato insertado correctamente", "datos": datos}), 201  # Código 201: Recurso creado

@app.route("/grafica")
def grafica_h():
    with open(json_file, "r") as txt:
        porcentaje = json.load(txt)
    for i in porcentaje:
     if "Hydro (% equivalent primary energy)" in i:
                    energia.append(i["Hydro (% equivalent primary energy)"])

    plt.figure(figsize=(6, 4))
    plt.hist(energia, bins=5, color="#44bba1")
    plt.title("Porcentaje de energía hidroeléctrica")
    plt.xlabel("Porcentaje (%)")
    plt.ylabel("Frecuencia")


    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    
    return Response(img.getvalue(), mimetype='image/png')

if __name__ == '__main__':
 app.run(debug=True, port=5000)
