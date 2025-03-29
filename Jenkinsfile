pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Angad0691996/My_first_CICD_Pipeline.git'
        SUBSCRIBER_DIR = 'iot-subscriber'
        DOCKER_IMAGE = 'angad069/iot-subscriber:latest'
    }

    stages {
        stage('Clone Repository') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    script {
                        if (fileExists("${SUBSCRIBER_DIR}/.git")) {
                            echo "Directory exists, pulling latest changes..."
                            sh """
                                cd ${SUBSCRIBER_DIR}
                                git pull https://$GIT_USER:$GIT_PASS@github.com/Angad0691996/My_first_CICD_Pipeline.git main
                            """
                        } else {
                            echo "Cloning repository..."
                            sh "git clone https://$GIT_USER:$GIT_PASS@github.com/Angad0691996/My_first_CICD_Pipeline.git ${SUBSCRIBER_DIR}"
                        }
                    }
                }
            }
        }

        stage('Install Dependencies & Docker') {
            steps {
                script {
                    sh '''
                        echo "Updating system and installing Docker..."
                        sudo apt-get update -y
                        sudo apt-get install -y docker.io
                        sudo systemctl start docker
                        sudo systemctl enable docker
                        sudo usermod -aG docker $USER
                        echo "Docker installed successfully!"
                    '''
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    sh """
                        cd ${SUBSCRIBER_DIR}
                        echo "Building Docker image..."
                        docker build -t ${DOCKER_IMAGE} .
                        echo "Pushing image to Docker Hub..."
                        docker push ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Run IoT Subscriber in Docker') {
            steps {
                script {
                    sh """
                        echo "Stopping existing container..."
                        docker stop iot-subscriber || true
                        docker rm iot-subscriber || true
                        echo "Running new IoT Subscriber container..."
                        docker run -d --name iot-subscriber -p 1883:1883 ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Reminder to Start IoT Publisher') {
            steps {
                script {
                    echo "🚀 REMINDER: Start the IoT Publisher manually on your Windows laptop."
                }
            }
        }

        stage('Monitor Logs') {
            steps {
                script {
                    sh "docker logs -f iot-subscriber"
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Build failed! Check logs for errors.'
        }
        success {
            echo '✅ Build and deployment successful!'
        }
    }
}
