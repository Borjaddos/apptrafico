from flask import Flask, jsonify, render_template
import psycopg2 
import os

app = Flask(__name__)   

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map_data/<fecha>')
def map_data(fecha):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT prediction, Description, X, Y 
        FROM predicciones 
        WHERE Fecha_Hora::date = %s
    """, (fecha,))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Transformamos los datos en un formato adecuado
    points = []
    for row in rows:
        prediction, description, x, y = row
        points.append({
            'prediction': prediction,
            'description': description,
            'x': x,
            'y': y
        })

    return jsonify(points)

if __name__ == '__main__':
    app.run(debug=True)

