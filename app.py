from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Usar la variable de entorno para la URL de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener las localizaciones desde la base de datos
@app.route('/get_locations')
def get_locations():
    # Conectar a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Ejecutar consulta para obtener los puntos geoespaciales
    cur.execute("SELECT id, name, latitude, longitude FROM locations;")
    locations = cur.fetchall()

    # Cerrar la conexión
    cur.close()
    conn.close()

    # Devolver los datos en formato JSON
    return jsonify([{
        'id': loc[0],
        'name': loc[1],
        'latitude': loc[2],
        'longitude': loc[3]
    } for loc in locations])

# Ruta para buscar localizaciones por nombre
@app.route('/search_location', methods=['GET'])
def search_location():
    query = request.args.get('query', '')  # Obtener el parámetro de búsqueda

    # Conectar a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Ejecutar consulta con el parámetro de búsqueda
    cur.execute("SELECT id, name, latitude, longitude FROM locations WHERE name ILIKE %s;", ('%' + query + '%',))
    locations = cur.fetchall()

    # Cerrar la conexión
    cur.close()
    conn.close()

    # Devolver los resultados en formato JSON
    return jsonify([{
        'id': loc[0],
        'name': loc[1],
        'latitude': loc[2],
        'longitude': loc[3]
    } for loc in locations])

if __name__ == '__main__':
    app.run(debug=True)
