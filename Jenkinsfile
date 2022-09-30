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
        stage('Update GIT') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        withCredentials([usernamePassword(credentialsId: '829f6427-a474-48c2-a120-d02b4b6e5da2', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                            def encodedPassword = URLEncoder.encode("$GIT_PASSWORD",'UTF-8')
                            sh "git config user.email jenkins@localhost"
                            sh "git config user.name jenkins"
                            sh "git add ."
                            sh "git commit -m 'Triggered Build: ${env.BUILD_NUMBER}'"
                            sh "git push https://$GIT_USERNAME:${encodedPassword}@github.com/$GIT_USERNAME/example.git HEAD:origin/master"
                        }
                    }
                }
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