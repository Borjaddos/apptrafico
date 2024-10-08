from flask import Flask,jsonify
import psycopg2 
import os

app = Flask(__name__)   

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return "Hola Mundo"

@app.route('/db')
def db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    current_time = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"current_time":current_time})

if __name__ == '__main__':
    app.run(debug=True)