from flask import Flask, render_template, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    fecha_actual = datetime.now()
    return render_template('index.html', fecha_actual=fecha_actual)

@app.route('/map_data/<string:fecha>/<string:hora>', methods=['GET'])
def map_data(fecha, hora):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Cambia el formato de la fecha y hora a un timestamp
    fecha_hora = f"{fecha} {hora}"

    query = """
    SELECT X, Y, ida, vuelta, Description, Estacion
    FROM predicciones
    WHERE Fecha_Hora = %s;
    """
    cur.execute(query, (fecha_hora,))
    results = cur.fetchall()

    cur.close()
    conn.close()

    puntos = []
    for row in results:
        puntos.append({
            "X": row[0],
            "Y": row[1],
            "ida": row[2],
            "vuelta": row[3],
            "description": row[4],
            "estacion": row[5]
        })

    return jsonify(puntos)

@app.route('/next_prediction/<int:threshold>', methods=['GET'])
def next_prediction(threshold):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    query = """
    SELECT *
    FROM predicciones
    WHERE (ida > %s OR vuelta > %s) AND Fecha_Hora > NOW()
    ORDER BY Fecha_Hora
    LIMIT 1;
    """
    cur.execute(query, (threshold, threshold))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return jsonify({
            "estacion": result[5],  # Cambia el índice según la posición de "Estacion"
            "fecha_hora": result[0].isoformat(),  # Convertir a ISO para formato legible
            "ida": result[1],
            "vuelta": result[2]
        })
    else:
        return jsonify({"error": "No hay predicciones próximas que superen el umbral."})

if __name__ == '__main__':
    app.run(debug=True)

