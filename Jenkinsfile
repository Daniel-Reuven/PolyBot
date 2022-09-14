pipeline {
    agent any

    stages {
        stage('Build Bot app') {
            steps {
               sh '''
                    aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 352708296901.dkr.ecr.eu-central-1.amazonaws.com
                    docker build -t danielreuven-polybot:0.0.$BUILD_TAG .
                    docker tag danielreuven-polybot:0.0.$BUILD_TAG 352708296901.dkr.ecr.eu-central-1.amazonaws.com/danielreuven-polybot:0.0.$BUILD_TAG
                    docker push 352708296901.dkr.ecr.eu-central-1.amazonaws.com/danielreuven-polybot:0.0.$BUILD_TAG

               '''
            }
        }
        stage('Stage II') {
            steps {
                sh 'echo "stage II..."'
            }
        }
        stage('Stage III ...') {
            steps {
                sh 'echo echo "stage III..."'
            }
        }
    }
}