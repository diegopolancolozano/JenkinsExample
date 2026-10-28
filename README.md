# JenkinsExample: tienda con Flask y SQLite

Una tienda pequeña para demostrar integración y despliegue continuo: permite agregar productos y consultar el catálogo. SQLite guarda los productos en un archivo; no hay un servidor de base de datos separado. El volumen Docker conserva el archivo entre reinicios y despliegues normales.

## Ejecutar con Docker

Con Docker Desktop iniciado y Compose disponible:

```bash
docker compose up -d --build
```

Abra http://localhost:5000, agregue un producto y actualice la página. Para detener la aplicación sin borrar la base: `docker compose down`. No use `docker compose down -v` si desea conservar los datos.

## Ejecutar sin Docker

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

En Windows puede usar `py -m venv .venv` y `.venv\Scripts\Activate.ps1`. La base se crea en `data/tienda.db`. Las pruebas usan bases temporales independientes:

```bash
python -m unittest discover -v
```

## Pipeline en Jenkins

Requisitos: Jenkins con plugins Pipeline y Git; un agente Linux con Docker, Docker Compose y permisos para usar el daemon; acceso a GitHub y PyPI; y puerto 5000 libre en el host del agente. El despliegue se ejecuta en ese host, no en un servidor externo. La base SQLite vive en el volumen Docker `tienda_datos`; preparar la base crea la tabla si no existe y no borra los productos.

1. Cree una tarea **Pipeline** y seleccione **Pipeline script from SCM** → Git.
2. Configure `https://github.com/diegopolancolozano/JenkinsExample.git`, la rama `main` y la ruta `Jenkinsfile`.
3. Ejecute **Construir ahora** una primera vez. El archivo configura `pollSCM` para consultar cambios aproximadamente cada dos minutos; un webhook accesible es otra opción.
4. Revise las etapas: obtener código, construir imagen, pruebas, preparar la base, desplegar y verificar que responde.
5. Acceda a `http://IP_DEL_AGENTE:5000` desde un equipo con conectividad. Si Jenkins corre en un contenedor, `localhost` dentro de Jenkins no es necesariamente el host.

La primera ejecución puede tardar por la descarga de la imagen y dependencias. Cada ejecución reconstruye la imagen, realiza las pruebas con una base temporal y, solo si pasan, prepara la base persistente y actualiza la aplicación. La comprobación final hace una solicitud HTTP desde el contenedor.

## Demostración

1. Muestre el repositorio y explique `app.py`, `test_app.py`, `Dockerfile`, `compose.yaml` y `Jenkinsfile`.
2. Ejecute el pipeline y muestre las etapas. Abra la tienda, agregue un producto y actualice para demostrar la persistencia.
3. Introduzca un error controlado en la validación, haga commit y push y observe que fallan las pruebas antes del despliegue. Corrija el error y suba otro commit.
4. Tras el nuevo despliegue, compruebe que el producto anterior sigue en el catálogo.

SQLite es apropiada para esta demostración de una sola aplicación. El servidor de desarrollo de Flask y el despliegue local no son una configuración de producción.
