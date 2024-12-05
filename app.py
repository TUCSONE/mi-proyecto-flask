from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bienvenido a la página de verificación.'

# Ruta para mostrar el mensaje verificado para cada invitado
@app.route('/verificado/<nombre>')
def verificado(nombre):
    return f"Invitado: {nombre} - ¡Verificado!"

if __name__ == '__main__':
    app.run(debug=True)

# Configurar base de datos
import os

DB_NAME = os.path.join(os.getcwd(), "database.db")


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Generar un código QR para cada invitado
def generate_qr(name):
    qr_code = qrcode.make(name)
    qr_path = f'static/{name}.png'
    qr_code.save(qr_path)
    return qr_path

# Función para agregar invitados
def add_guest(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Generar código QR y añadir a la base de datos
    qr_code = f"{name}_QR"
    try:
        cursor.execute('''
            INSERT INTO guests (name, code)
            VALUES (?, ?)
        ''', (name, qr_code))
        conn.commit()
        print(f"Invitado {name} añadido exitosamente.")
        generate_qr(qr_code)  # Generar el código QR
    except sqlite3.IntegrityError:
        print(f"Error: El invitado '{name}' ya existe.")
    finally:
        conn.close()

# Ruta para el formulario de agregar invitados
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_guest', methods=['POST'])
def add_guest_route():
    name = request.form.get('name')
    if name:
        add_guest(name)
        return render_template('success.html', name=name)
    return "Error: Nombre no válido.", 400

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
import os
from flask import Flask, render_template, request
import sqlite3
import os
from generador_qr import generate_qr  # Importa la función para generar los QR

app = Flask(__name__)

# Configuración de la base de datos
DB_NAME = os.path.join(os.getcwd(), "database.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para agregar invitados a la base de datos
def add_guest(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    qr_code = f"{name}_QR"
    try:
        cursor.execute('''
            INSERT INTO guests (name, code)
            VALUES (?, ?)
        ''', (name, qr_code))
        conn.commit()
        print(f"Invitado {name} añadido exitosamente.")
        generate_qr(name)  # Generar el código QR para el invitado
    except sqlite3.IntegrityError:
        print(f"Error: El invitado '{name}' ya existe.")
    finally:
        conn.close()

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para agregar un invitado y generar el código QR
@app.route('/add_guest', methods=['POST'])
def add_guest_route():
    name = request.form.get('name')
    if name:
        add_guest(name)
        return render_template('success.html', name=name)
    return "Error: Nombre no válido.", 400

# Ruta para mostrar el mensaje verificado para cada invitado
@app.route('/verificado/<nombre>')
def verificado(nombre):
    return f"Invitado: {nombre.replace('_', ' ')} - ¡Verificado!"

if __name__ == "__main__":
    init_db()  # Inicializar la base de datos
    app.run(debug=True)
