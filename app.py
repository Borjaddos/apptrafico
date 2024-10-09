from flask import Flask, render_template, jsonify, request
import psycopg2 
import os

app = Flask(__name__)   

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map-data')
def map_data():
    # Obtiene la fecha y hora de la consulta
    datetime = request.args.get('datetime')
    
    # Conexión a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Consulta para obtener datos para la fecha y hora seleccionadas
    cur.execute("""
        SELECT Fecha_Hora, prediction, Description, X, Y 
        FROM predicciones 
        WHERE Fecha_Hora = %s;
    """, (datetime,))

    rows = cur.fetchall()

    # Cierra la conexión
    cur.close()
    conn.close()

    # Prepara los datos para el mapa
    map_points = []
    for row in rows:
        timestamp, prediction, description, x, y = row
        map_points.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": prediction,
            "description": description,
            "x": x,
            "y": y
        })

    return jsonify(map_points)

if __name__ == '__main__':
    app.run(debug=True)
