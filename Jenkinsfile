pipeline {
    agent any
    environment {
        REGISTRY_URL = "352708296901.dkr.ecr.eu-central-1.amazonaws.com"
        IMAGE_TAG = "0.0.$BUILD_NUMBER"
        IMAGE_NAME = "daniel-reuven-ecr"
    }
    stages {
        stage('Build Bot app') {
            steps {
               sh '''
                    aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 352708296901.dkr.ecr.eu-central-1.amazonaws.com
                    docker build -t $IMAGE_NAME .
                    docker tag $IMAGE_NAME $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
                    docker push $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
               '''
            }
        }
        stage('Trigger Deploy') {
            steps {
                build job: BotDeploy, wait: false, parameters: [
                string(name: 'current-ecr-img-name', value: "$IMAGE_NAME:$IMAGE_TAG")
                ]
            }
        }
    }
    post{
        always {
            sh '''
                echo "Post - Always section - remove the container from jenkins1"
                docker rmi $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
            '''
        }
    }
}