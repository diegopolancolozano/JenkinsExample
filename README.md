# JenkinsExample

Aplicación web Flask para demostrar CI y entrega de un artefacto con Jenkins. Incluye dos funciones: sumar números y comprobar si una frase es un palíndromo. La aplicación no guarda información y el pipeline no despliega automáticamente a un servidor.

## Ejecutar la aplicación

Se necesita Python 3 con soporte para `venv` y acceso a PyPI para instalar Flask.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`. En Windows, cree el entorno con `py -m venv .venv` y actívelo con `.venv\Scripts\Activate.ps1`.

## Ejecutar pruebas

```bash
python -m unittest discover -v
```

Las pruebas cubren la lógica, decimales, entradas inválidas y respuestas HTTP de los dos formularios usando el cliente de pruebas de Flask.

## Configurar Jenkins

1. Use Jenkins con plugins Pipeline y Git, y un agente Linux con Git, Python 3, `venv` y acceso a PyPI.
2. Cree una tarea **Pipeline**. En **Pipeline script from SCM**, elija Git, indique la URL del repositorio y la rama `main`; use credenciales si corresponde.
3. Deje `Jenkinsfile` como ruta y ejecute **Construir ahora** una primera vez.
4. Revise la salida de consola y las etapas: código, dependencias, validación, pruebas y empaquetado. Una ejecución exitosa guarda `aplicacion.zip` como artefacto.

El archivo consulta Git aproximadamente cada dos minutos con `pollSCM`; la primera ejecución manual carga ese disparador. Como alternativa, configure un webhook de GitHub si Jenkins es accesible desde allí. El pipeline usa `sh` y `.venv/bin/python`, por lo que un agente Windows requiere adaptar los comandos.

## Demostración

1. Muestre la aplicación en el navegador y pruebe `2.5 + 3` y `Anita lava la tina`.
2. Ejecute el pipeline y muestre las pruebas y el ZIP archivado.
3. Cambie temporalmente la suma para introducir un error, haga commit y push y observe que falla la etapa de pruebas.
4. Corrija el error, suba otro commit y muestre una ejecución exitosa. Compruebe cada resultado en Jenkins.

El ZIP contiene el código, la plantilla y las instrucciones para su ejecución; es un artefacto de entrega, no un despliegue. La instalación y ejecución de Jenkins no están incluidas en el repositorio.
