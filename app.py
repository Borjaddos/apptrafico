from flask import Flask, jsonify, render_template, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map-data')
def map_data():
    # Obtener la fecha y hora seleccionada por el usuario
    datetime_str = request.args.get('datetime')
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Obtener los puntos para la fecha y hora seleccionada
    query = """
        SELECT Fecha_Hora, prediction, Description, X, Y
        FROM predicciones
        WHERE Fecha_Hora = %s
    """
    cur.execute(query, (datetime_str,))
    results = cur.fetchall()

    # Formato de los resultados
    data = []
    for row in results:
        data.append({
            'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S'),
            'prediction': row[1],
            'description': row[2],
            'x': row[3],
            'y': row[4]
        })

    # Obtener la próxima predicción mayor a 400 después de la hora actual
    current_time = datetime.now()
    query_next_prediction = """
        SELECT Fecha_Hora, prediction, Description, X, Y
        FROM predicciones
        WHERE prediction > 400 AND Fecha_Hora > %s
        ORDER BY Fecha_Hora ASC LIMIT 1
    """
    cur.execute(query_next_prediction, (current_time,))
    next_prediction = cur.fetchone()

    conn.close()

    return jsonify({'data': data, 'next_prediction': next_prediction})

if __name__ == '__main__':
    app.run(debug=True)
