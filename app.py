from flask import Flask
import psycopg2

app = Flask(__name__)


DATABASE_CONFIG = {
    'dbname': 'flask-postgres-prueba',
    'user': 'postgres',
    'password': 'SQLkenyo90',
    'host': 'localhost',
    'port': 5432
}
def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG) # psycopg2 es para la coneccion a la base de datos
    return conn

def create_user_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print('Table user create successfuly..!')

    except Exception as e:
        print(f"Error creating table: {e}")

create_user_table()

@app.get('/users')
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users, 200

    except Exception as e:
        return {'error':str(e)},500

if __name__ == "__main__":
    app.run(debug=True)  