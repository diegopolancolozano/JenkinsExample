# JenkinsExample: tienda con Flask y SQLite

Tienda pequeña para demostrar integración y despliegue continuo con Jenkins. Permite agregar productos y consultar el catálogo. Los datos se guardan en SQLite, dentro de un volumen Docker, por lo que sobreviven a reinicios y a nuevos despliegues.

## Estructura

| Archivo | Propósito |
| --- | --- |
| `app.py` | Aplicación Flask: catálogo, formulario y validación de productos. |
| `init_db.py` | Crea la tabla de productos si no existe, sin borrar datos. |
| `test_app.py` | Pruebas unitarias; cada una usa una base temporal. |
| `templates/index.html` | Página de la tienda. |
| `Dockerfile` | Imagen de la aplicación. |
| `compose.yaml` | Servicio `tienda` en el puerto 5000 y volumen de datos. |
| `Jenkinsfile` | Pipeline de construcción, pruebas y despliegue. |

## Ejecutar con Docker

```bash
docker compose up -d --build
```

Abra http://localhost:5000, agregue un producto y recargue la página.

- Detener sin perder datos: `docker compose down`
- Detener **y borrar** los datos: `docker compose down -v`

## Ejecutar sin Docker

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

En Windows: `py -m venv .venv` y `.venv\Scripts\Activate.ps1`. La base se crea en `data/tienda.db`.

Pruebas:

```bash
python -m unittest discover -v
```

## Pipeline en Jenkins

Requisitos: Jenkins con los plugins Pipeline y Git, y un agente con Docker y Docker Compose. La aplicación se despliega en la misma máquina donde corre el agente.

### Configurar la tarea

1. En Jenkins, cree una tarea de tipo **Pipeline**.
2. En *Definition* elija **Pipeline script from SCM** → **Git**.
3. Repositorio: `https://github.com/diegopolancolozano/JenkinsExample.git`, rama `main`, ruta del script `Jenkinsfile`.
4. Guarde y ejecute **Construir ahora** una primera vez. A partir de ahí, Jenkins revisa el repositorio cada ~2 minutos (`pollSCM`) y lanza el pipeline cuando hay commits nuevos.

### Etapas

| Etapa | Qué hace |
| --- | --- |
| Obtener código | Descarga el commit a construir. |
| Construir imagen | `docker compose build` |
| Pruebas | Ejecuta las pruebas dentro de la imagen recién construida. Si fallan, el pipeline se detiene y **no se despliega**. |
| Preparar base de datos | Crea la tabla en el volumen persistente si no existe. |
| Desplegar aplicación | `docker compose up -d` reemplaza el contenedor por la nueva versión. |
| Verificar despliegue | Hace una petición HTTP a la app y falla si no responde tras ~20 s. |

Cuando termine, abra `http://IP_DEL_AGENTE:5000` (o `http://localhost:5000` si el agente es su propia máquina). La primera ejecución tarda más porque descarga la imagen base y las dependencias.

## Guion de demostración

1. Recorra el repositorio y explique `app.py`, `test_app.py`, `Dockerfile`, `compose.yaml` y `Jenkinsfile`.
2. Ejecute el pipeline y muestre cada etapa en Jenkins. Abra la tienda y agregue un producto.
3. Introduzca un error a propósito (por ejemplo, permitir precios negativos en `validar_producto`), haga commit y push. El pipeline falla en **Pruebas** y la versión desplegada no cambia.
4. Corrija el error y haga otro push. El pipeline pasa y despliega la nueva versión.
5. Recargue la tienda: el producto agregado antes sigue ahí, porque la base vive en el volumen.

## Notas

SQLite es suficiente para una aplicación de demostración con una sola instancia. El servidor de desarrollo de Flask no está pensado para producción.
