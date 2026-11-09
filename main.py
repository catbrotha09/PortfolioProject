# Import
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre,
            contacto,
            texto
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# Página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    skill_selected = request.form.get('skill_selected')
    exito = False
    
    if request.method == 'POST' and 'nombre' in request.form:
        nombre = request.form.get('nombre')
        contacto = request.form.get('contacto')
        texto = request.form.get('texto')
        
        if texto:
            conn = get_db_connection()
            conn.execute('INSERT INTO diario (nombre, contacto, texto) VALUES (?, ?, ?)',
                         (nombre, contacto, texto))
            conn.commit()
            conn.close()
            exito = True
    
    return render_template('index.html', skill_selected=skill_selected, exito=exito)


if __name__ == "__main__":
    app.run(debug=True)