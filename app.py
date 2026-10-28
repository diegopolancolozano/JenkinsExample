"""Aplicación Flask para demostrar integración y entrega continua."""
from decimal import Decimal, InvalidOperation
import unicodedata
from flask import Flask, render_template, request

app = Flask(__name__)


def sumar(primero: str, segundo: str) -> Decimal:
    try:
        a, b = Decimal(primero.strip()), Decimal(segundo.strip())
    except (InvalidOperation, AttributeError, ValueError) as exc:
        raise ValueError("Ingresa dos números válidos.") from exc
    if not a.is_finite() or not b.is_finite():
        raise ValueError("Ingresa dos números finitos.")
    return a + b


def es_palindromo(texto: str) -> bool:
    caracteres = unicodedata.normalize("NFD", texto.casefold())
    limpio = "".join(c for c in caracteres if c.isalnum())
    if not limpio:
        raise ValueError("Escribe una palabra o frase con letras o números.")
    return limpio == limpio[::-1]


@app.get("/")
def inicio():
    return render_template("index.html")


@app.post("/sumar")
def calcular_suma():
    try:
        resultado = sumar(request.form.get("primero", ""), request.form.get("segundo", ""))
        return render_template("index.html", suma=resultado)
    except ValueError as exc:
        return render_template("index.html", error_suma=str(exc)), 400


@app.post("/palindromo")
def comprobar_palindromo():
    try:
        resultado = es_palindromo(request.form.get("texto", ""))
        return render_template("index.html", palindromo=resultado)
    except ValueError as exc:
        return render_template("index.html", error_palindromo=str(exc)), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
