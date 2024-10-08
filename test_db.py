import psycopg2
import os

# Define tu URL de conexión a la base de datos
DATABASE_URL = "postgresql://midb_9oqp_user:rfJeUk8tCjR7901mCItUuVEq3mvzaRho@dpg-cs2mj38gph6c73866np0-a.frankfurt-postgres.render.com/midb_9oqp"

# Conexión a la base de datos
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Ejecutar una consulta de prueba
    cur.execute("SELECT NOW();")
    current_time = cur.fetchone()
    print("Hora actual:", current_time)

    # Cerrar conexión
    cur.close()
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos:", e)
