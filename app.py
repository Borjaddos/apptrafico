from flask import Flask, jsonify, render_template
import psycopg2
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map_data/<fecha>/<hora>')
def map_data(fecha, hora):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Convertir fecha y hora a un timestamp
    timestamp = f"{fecha} {hora}:00"

    # Consulta para obtener datos de las estaciones
    cur.execute("""
        SELECT Estacion, X, Y, ida, vuelta, Description
        FROM predicciones
        WHERE Fecha_Hora = %s
    """, (timestamp,))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # Crear una lista de puntos de datos
    points = []
    for row in rows:
        point = {
            'estacion': row[0],
            'x': row[1],
            'y': row[2],
            'ida': row[3],
            'vuelta': row[4],
            'description': row[5],
        }
        points.append(point)

    return jsonify(points)

@app.route('/next_prediction/<threshold>')
def next_prediction(threshold):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Obtener la hora actual
    now = datetime.now()
    
    # Consultar el próximo valor que supere el umbral
    cur.execute("""
        SELECT Estacion, Fecha_Hora, ida, vuelta
        FROM predicciones
        WHERE (ida > %s OR vuelta > %s) AND Fecha_Hora > %s
        ORDER BY Fecha_Hora
        LIMIT 1
    """, (threshold, threshold, now))

    next_prediction = cur.fetchone()
    cur.close()
    conn.close()
    
    if next_prediction:
        return jsonify({
            'estacion': next_prediction[0],
            'fecha_hora': next_prediction[1],
            'ida': next_prediction[2],
            'vuelta': next_prediction[3]
        })
    else:
        return jsonify({'error': 'No hay predicciones próximas que superen el umbral.'})

if __name__ == '__main__':
    app.run(debug=True)
