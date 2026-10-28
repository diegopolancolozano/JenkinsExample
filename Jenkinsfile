pipeline {
    agent any
    triggers { pollSCM('H/2 * * * *') }
    stages {
        stage('Obtener código') {
            steps { checkout scm }
        }
        stage('Construir imagen') {
            steps { sh 'docker compose build' }
        }
        stage('Pruebas') {
            steps { sh 'docker compose run --rm --no-deps tienda python -m unittest discover -v' }
        }
        stage('Preparar base de datos') {
            steps { sh 'docker compose run --rm --no-deps tienda python init_db.py' }
        }
        stage('Desplegar aplicación') {
            steps { sh 'docker compose up -d --no-build tienda' }
        }
        stage('Verificar despliegue') {
            steps {
                sh '''#!/bin/sh
                set -eu
                for intento in 1 2 3 4 5 6 7 8 9 10; do
                    if docker compose exec -T tienda python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/', timeout=2)"; then
                        echo "Aplicación disponible."
                        exit 0
                    fi
                    sleep 2
                done
                echo "La aplicación no respondió."
                exit 1
                '''
            }
        }
    }
}
