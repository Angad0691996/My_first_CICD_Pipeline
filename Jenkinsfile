pipeline {
    agent any

    environment {
        INSTALL_DIR = '/opt/iot-app'
        VENV_DIR = '/opt/iot-app/venv'
    }

    stages {
        stage('Install System Packages') {
            steps {
                sh '''
                sudo apt update && sudo apt install -y python3 python3-venv python3-pip
                '''
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                # Create installation directory if not exists
                sudo mkdir -p ${INSTALL_DIR}

                # Create virtual environment if not exists
                if [ ! -d "${VENV_DIR}" ]; then
                    python3 -m venv ${VENV_DIR}
                fi

                # Activate venv and install required packages
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install AWSIoTPythonSDK Flask Flask-MySQLdb Flask-SocketIO paho-mqtt mysql-connector-python mysqlclient eventlet greenlet python-socketio
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
            echo '✅ Python Virtual Environment & Dependencies Successfully Installed on Jenkins EC2!'
        }
        failure {
            echo '❌ Installation Failed! Check logs for errors.'
        }
    }
}
