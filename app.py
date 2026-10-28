"""Tienda pequeña con persistencia SQLite para demostrar Jenkins."""
import os
import sqlite3
from decimal import Decimal, InvalidOperation
from pathlib import Path
from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['DATABASE'] = os.environ.get('DATABASE_PATH', 'data/tienda.db')


def conexion():
    if 'db' not in g:
        ruta = Path(app.config['DATABASE'])
        ruta.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(str(ruta))
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar_conexion(_error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def inicializar_bd():
    db = conexion()
    db.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, precio_centavos INTEGER NOT NULL CHECK(precio_centavos > 0))')
    db.commit()


def validar_producto(nombre, precio):
    nombre = nombre.strip()
    if not nombre or len(nombre) > 100:
        raise ValueError('El nombre debe contener entre 1 y 100 caracteres.')
    try:
        cantidad = Decimal(precio.strip())
        if not cantidad.is_finite() or cantidad <= 0 or cantidad > Decimal('9999999.99') or cantidad.as_tuple().exponent < -2:
            raise ValueError('El precio debe ser positivo y tener máximo dos decimales.')
        centavos = int(cantidad * 100)
    except (InvalidOperation, AttributeError):
        raise ValueError('Ingresa un precio válido.') from None
    return nombre, centavos


@app.get('/')
def inicio():
    productos = conexion().execute('SELECT id, nombre, precio_centavos FROM productos ORDER BY id DESC').fetchall()
    return render_template('index.html', productos=productos)


@app.post('/productos')
def agregar_producto():
    try:
        nombre, precio = validar_producto(request.form.get('nombre', ''), request.form.get('precio', ''))
    except ValueError as exc:
        productos = conexion().execute('SELECT id, nombre, precio_centavos FROM productos ORDER BY id DESC').fetchall()
        return render_template('index.html', productos=productos, error=str(exc)), 400
    db = conexion()
    db.execute('INSERT INTO productos (nombre, precio_centavos) VALUES (?, ?)', (nombre, precio))
    db.commit()
    return redirect(url_for('inicio'))


if __name__ == '__main__':
    with app.app_context():
        inicializar_bd()
    app.run(host='0.0.0.0', port=5000)
