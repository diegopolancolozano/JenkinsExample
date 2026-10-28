pipeline {
    agent any
    triggers { pollSCM('H/2 * * * *') }
    stages {
        stage('Obtener código') {
            steps { checkout scm }
        }
        stage('Validar aplicación') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m py_compile app.py'
                sh 'python3 app.py'
            }
        }
        stage('Ejecutar pruebas') {
            steps { sh 'python3 -m unittest discover -v' }
        }
        stage('Empaquetar') {
            steps {
                sh 'python3 -m zipfile -c aplicacion.zip app.py'
                archiveArtifacts artifacts: 'aplicacion.zip', fingerprint: true
            }
        }
    }
}

