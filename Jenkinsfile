pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Angad0691996/My_first_CICD_Pipeline.git'
        BRANCH = 'main'
        APP_DIR = "${WORKSPACE}/iot-subscriber"
    }

    stages {
        stage('Clone Repository') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh """
                    if [ -d "${APP_DIR}/.git" ]; then
                        echo "Directory exists, pulling latest changes..."
                        cd ${APP_DIR} && git pull origin ${BRANCH}
                    else
                        echo "Cloning repository..."
                        git clone https://${GIT_USER}:${GIT_PASS}@github.com/Angad0691996/My_first_CICD_Pipeline.git ${APP_DIR}
                    fi
                    """
                }
            }
        }

        stage('Install Dependencies & Docker') {
            steps {
                sh """
                echo "Updating system packages..."
                echo '${GIT_PASS}' | sudo -S apt update
                echo "Installing Python dependencies..."
                sudo -S apt install -y python3-pip
                pip3 install -r ${APP_DIR}/requirements.txt

                echo "Checking if Docker is installed..."
                if ! command -v docker &> /dev/null; then
                    echo "Installing Docker..."
                    sudo -S apt install -y docker.io
                    sudo systemctl start docker
                    sudo systemctl enable docker
                    sudo usermod -aG docker jenkins
                else
                    echo "Docker is already installed."
                fi
                """
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                }
            }
        }

        stage('Run IoT Subscriber in Docker') {
            steps {
                sh """
                cd ${APP_DIR}
                echo "Building Docker image..."
                docker build -t iot-subscriber .
                echo "Restarting Docker container..."
                docker stop iot-subscriber || true
                docker rm iot-subscriber || true
                docker run -d --name iot-subscriber iot-subscriber
                """
            }
        }

        stage('Reminder to Start IoT Publisher') {
            steps {
                echo "IoT Publisher runs on Windows. Please start it manually!"
            }
        }

        stage('Monitor Logs') {
            steps {
                sh "docker logs -f iot-subscriber || tail -n 100 ${APP_DIR}/logs/subscriber.log"
            }
        }
    }

    post {
        success {
            echo "Deployment successful! Remember to start the IoT Publisher on Windows."
        }
        failure {
            echo "Build failed! Check logs."
        }
    }
}
