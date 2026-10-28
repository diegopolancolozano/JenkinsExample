"""Una función sencilla para ilustrar integración continua."""

def saludo(nombre: str) -> str:
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    return f"Hola, {nombre}. Jenkins ejecutó esta aplicación."

if __name__ == "__main__":
    print(saludo("Infraestructura III"))
