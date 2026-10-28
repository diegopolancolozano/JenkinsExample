# JenkinsExample

Ejemplo sencillo de integración continua y entrega de un artefacto con Jenkins, Git y Python. No realiza un despliegue automático a un servidor.

## Requisitos

- Jenkins con un agente Linux que tenga Git y Python 3 disponibles.
- Plugins Pipeline y Git instalados y configurados en Jenkins.
- Un repositorio Git accesible desde Jenkins. Este proyecto usa `Jenkinsfile` en su raíz.

## Probar localmente

```bash
python3 app.py
python3 -m unittest discover -v
```

En Windows se puede sustituir `python3` por `py`.

## Configurar el pipeline

1. Suba estos archivos al repositorio y anote la rama usada.
2. En Jenkins seleccione **Nueva tarea → Pipeline**.
3. En **Pipeline**, seleccione **Pipeline script from SCM**, elija Git y escriba la URL y la rama del repositorio. Use credenciales si el repositorio es privado.
4. Deje `Jenkinsfile` como ruta del script y ejecute **Construir ahora** una primera vez.
5. Consulte las etapas y la salida de consola. Tras pasar las pruebas, Jenkins conserva `aplicacion.zip` como artefacto de la ejecución.

El `Jenkinsfile` consulta Git aproximadamente cada dos minutos mediante `pollSCM`; el primer arranque manual carga esta configuración. Para recibir cambios más rápido puede configurarse un webhook accesible desde GitHub; esa opción depende de la conectividad y configuración de Jenkins. Un agente Windows necesita reemplazar los pasos `sh` por `bat` o `powershell`.

## Demostración de resiliencia de las pruebas

Cambie temporalmente el texto devuelto por `saludo`, sin actualizar la prueba, y haga commit y push: la etapa de pruebas debe fallar y no se genera un nuevo artefacto exitoso. Restaure el texto, haga otro commit y compruebe que la ejecución vuelve a pasar. Los fallos y las ejecuciones deben verificarse en Jenkins; ejecutar las pruebas localmente no demuestra que el servidor esté configurado.

## Flujo

Git → Jenkins obtiene el código → valida Python → ejecuta pruebas → guarda el ZIP. El ZIP es una entrega para revisión o despliegue posterior; no equivale a desplegar la aplicación.
