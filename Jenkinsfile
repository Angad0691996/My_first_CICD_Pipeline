pipeline {
    agent any

    environment {
        GIT_CREDENTIALS_ID = 'github-credentials'
        SSH_CREDENTIALS_ID = 'ec2-ssh-key'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        DOCKER_IMAGE = 'angad0691996/iot-subscriber:latest'
        REPO_URL = 'https://github.com/Angad0691996/My_first_CICD_Pipeline.git'
        WORKDIR = 'iot-subscriber'
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    if (fileExists(WORKDIR)) {
                        echo 'Directory exists, pulling latest changes...'
                        dir(WORKDIR) {
                            withCredentials([usernamePassword(credentialsId: GIT_CREDENTIALS_ID, usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                                sh 'git pull https://${GIT_USER}:${GIT_PASS}@${REPO_URL} main'
                            }
                        }
                    } else {
                        echo 'Cloning repository...'
                        sh "git clone ${REPO_URL} ${WORKDIR}"
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
                        sudo usermod -aG docker jenkins
                        echo "Docker installed successfully!"
                    '''
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    dir(WORKDIR) {
                        sh '''
                            echo "Building Docker image..."
                            docker build -t $DOCKER_IMAGE .
                            echo "Pushing image to Docker Hub..."
                            docker push $DOCKER_IMAGE
                        '''
                    }
                }
            }
        }

        stage('Run IoT Subscriber in Docker') {
            steps {
                script {
                    sh '''
                        echo "Stopping existing container (if running)..."
                        docker stop iot-subscriber || true
                        docker rm iot-subscriber || true
                        echo "Starting new container..."
                        docker run -d --name iot-subscriber --restart unless-stopped $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Reminder to Start IoT Publisher') {
            steps {
                echo '✅ IoT Subscriber is running. Remember to start the IoT Publisher on your Windows laptop!'
            }
        }

        stage('Monitor Logs') {
            steps {
                script {
                    sh 'docker logs -f iot-subscriber'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Build failed! Check logs for errors.'
        }
    }
}
