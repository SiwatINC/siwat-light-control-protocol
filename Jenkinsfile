pipeline {
    agent any
  
    stages {
        stage('Clone') { 
            steps {
                git branch: 'main', url: 'https://git.siwatsystem.com/satitchula-stemlab/iot-lightstrip'
            }
        } 
        stage('Build Docker Image') {
            steps {
                script {
                    image = docker.build("siwatinc/siwat_light_control_protocol_server:latest"," --no-cache -f Dockerfile ./server-docker")
                }
            }
        }
        stage('Publish Docker Image') {
            steps {
                script {
                    docker.withRegistry("https://ghcr.io/v2") {
                        image.push()
                    }
                }
            }
        }
    }
}