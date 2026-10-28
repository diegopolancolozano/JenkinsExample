pipeline {
    agent any
    triggers { pollSCM('H/2 * * * *') }
    stages {
        stage('Obtener código') {
            steps { checkout scm }
        }
        stage('Preparar dependencias') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -r requirements.txt'
            }
        }
        stage('Validar aplicación') {
            steps { sh '.venv/bin/python -m py_compile app.py' }
        }
        stage('Ejecutar pruebas') {
            steps { sh '.venv/bin/python -m unittest discover -v' }
        }
        stage('Empaquetar') {
            steps {
                sh '.venv/bin/python -m zipfile -c aplicacion.zip app.py requirements.txt templates README.md'
                archiveArtifacts artifacts: 'aplicacion.zip', fingerprint: true
            }
        }
    }
}
