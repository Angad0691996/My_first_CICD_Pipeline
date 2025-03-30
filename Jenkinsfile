pipeline {
    agent any
    environment {
        APP_DIR = "/opt/iot-app"
        VENV_DIR = "$APP_DIR/venv"
    }
    stages {
        stage('Install System Packages') {
            steps {
                script {
                    sh '''
                        sudo apt update
                        sudo apt install -y python3 python3-venv python3-pip
                    '''
                }
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                script {
                    sh '''
                        sudo mkdir -p $APP_DIR
                        sudo chown -R jenkins:jenkins $APP_DIR  # Ensure Jenkins can write
                        
                        if [ ! -d "$VENV_DIR" ]; then
                            python3 -m venv $VENV_DIR
                        fi
                    '''
                }
            }
        }

        stage('Activate Virtual Env & Install Dependencies') {
            steps {
                script {
                    sh '''
                        source $VENV_DIR/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements_subscriber.txt || echo "requirements_subscriber.txt not found, skipping..."
                    '''
                }
            }
        }

        stage('Verify Installation') {
            steps {
                script {
                    sh '''
                        source $VENV_DIR/bin/activate
                        pip list
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Installation Failed! Check logs for errors."
        }
        success {
            echo "✅ Installation Successful!"
        }
    }
}
