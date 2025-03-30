pipeline {
    agent any

    environment {
        INSTALL_DIR = "/opt/iot-app"
        VENV_DIR = "$INSTALL_DIR/venv"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/Angad0691996/My_first_CICD_Pipeline.git'
            }
        }

        stage('Install System Packages') {
            steps {
                sh '''
                sudo apt update
                sudo apt install -y python3 python3-venv python3-pip
                '''
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                # Ensure the installation directory exists and has correct permissions
                sudo mkdir -p ${INSTALL_DIR}
                sudo chown -R jenkins:jenkins ${INSTALL_DIR}
                sudo chmod -R 755 ${INSTALL_DIR}

                # Create a virtual environment
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate

                # Upgrade pip and install dependencies
                pip install --upgrade pip
                pip install AWSIoTPythonSDK Flask Flask-MySQLdb Flask-SocketIO paho-mqtt \
                            mysql-connector-python mysqlclient eventlet greenlet python-socketio

                deactivate
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                pip list
                deactivate
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Installation Successful!"
        }
        failure {
            echo "❌ Installation Failed! Check logs for errors."
        }
    }
}
