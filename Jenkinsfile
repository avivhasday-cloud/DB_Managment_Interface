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
    }
    withCredentials([usernamePassword(credentialsId: 'git-pass-credentials-ID', passwordVariable: 'GIT_AUTHOR_NAME', usernameVariable: 'GIT_USERNAME')]) {
        sh("git checkout master")
        sh("git merge origin/dev")
        sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@my-repo.git --tags')
    }
    post {
        always {
            sh 'docker-compose down --remove-orphans -v'
            sh 'docker-compose ps'
        }
    }
}