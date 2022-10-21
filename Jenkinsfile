pipeline {
    agent {
        docker {
            label 'daniel-reuven-general'
            image '352708296901.dkr.ecr.eu-central-1.amazonaws.com/daniel-reuven-jenkins-agent:1'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    options {
        buildDiscarder(logRotator(daysToKeepStr: '30'))
        disableConcurrentBuilds()
        timestamps()
    }
    environment {
        REGISTRY_URL = "352708296901.dkr.ecr.eu-central-1.amazonaws.com"
        IMAGE_TAG = "0.0.$BUILD_NUMBER"
        IMAGE_NAME = "daniel-reuven-ecr"
    }
    stages {
        stage('Build Bot app') {
        options {
            timeout(time: 10, unit: 'MINUTES')
        }
            steps {
               sh '''
                    aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 352708296901.dkr.ecr.eu-central-1.amazonaws.com
                    docker build -t $IMAGE_NAME .
               '''
//                withCredentials([string(credentialsId: 'snyk', variable: 'ad811150-43d1-4bb1-b7c8-a9e8efba90fd')]) {
//                     sh '''
//                     snyk container test $IMAGE_NAME:$IMAGE_TAG --severity-threshold=high --file=Dockerfile
//                     '''
//                     }
               sh '''
                    docker tag $IMAGE_NAME $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
                    docker push $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
               '''
            }
        }
        stage('Trigger Deploy') {
            steps {
                build job: 'BotDeploy', wait: false, parameters: [
                string(name: 'BOT_IMAGE_NAME', value: "$REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG")
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