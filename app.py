from flask import Flask, render_template, jsonify, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Configura tu URL de base de datos aquí
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://tu_usuario:tu_contraseña@localhost:5432/tu_base_de_datos')

@app.route('/')
def index():
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()
    return render_template('index.html', fecha_actual=fecha_actual)

@app.route('/map_data')
def map_data():
    fecha = request.args.get('fecha')
    hora = request.args.get('hora')
    
    # Conectar a la base de datos y obtener los datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    query = """
    SELECT Fecha_Hora, ida, vuelta, Description, X, Y, Estacion
    FROM predicciones
    WHERE Fecha_Hora::date = %s AND EXTRACT(HOUR FROM Fecha_Hora) = %s
    """
    cur.execute(query, (fecha, int(hora.split(':')[0])))  # Solo obtenemos la hora
    rows = cur.fetchall()
    
    # Formatear los datos como una lista de diccionarios
    data = []
    for row in rows:
        data.append({
            'Fecha_Hora': row[0],
            'ida': row[1],
            'vuelta': row[2],
            'Description': row[3],
            'X': row[4],
            'Y': row[5],
            'Estacion': row[6]
        })
    
    cur.close()
    conn.close()
    
    return jsonify(data)

@app.route('/next_prediction')
def next_prediction():
    # Obtener la fecha y hora actuales
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Conectar a la base de datos y obtener la próxima predicción
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    query = """
    SELECT Fecha_Hora, ida, vuelta, Estacion
    FROM predicciones
    WHERE Fecha_Hora > %s AND (ida > 850 OR vuelta > 850)
    ORDER BY Fecha_Hora
    LIMIT 1
    """
    cur.execute(query, (current_time,))
    result = cur.fetchone()
    
    if result:
        prediction = {
            'Fecha_Hora': result[0],
            'ida': result[1],
            'vuelta': result[2],
            'Estacion': result[3]
        }
    else:
        prediction = None
    
    cur.close()
    conn.close()

    return jsonify(prediction)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
