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
                sh 'docker-compose up -d'
                sh 'sleep 15'
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
        stage("Deploy") {
            steps {
                sh 'git pull'
                sh 'git checkout origin/master'
                sh 'git merge origin/dev'
                sh 'git commit -m "merge dev to master after successfully build"'
                sh 'git push'
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