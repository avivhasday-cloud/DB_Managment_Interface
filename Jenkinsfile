pipeline {
    agent any
    stages {
        stage("Verify tooling") {
            steps {
                sh '''
                    docker info
                    docker version
                    docker-compose version
                '''
            }
        }
        stage("Prune Docker data") {
            steps {
                sh 'docker system prune -a --volumes -f'
            }
        }
        stage("Start container") {
            steps {
                sh 'docker-compose up -d --no-color'
                sh 'docker-compose ps'
            }
        }
        stage("Compile C code") {
            steps {
                sh '''
                    cd c
                    make clean
                    make 
                    cd ..
                '''
            }
        }
        stage("Test") {
            steps {
                sh 'echo $PWD'
                sh 'python3 -m unittest discover'
            }
        }
    }
    post {
        always {
            sh 'docker-compose down --remove-orphans -v'
            sh 'docker-compose ps'
        }
    }
}