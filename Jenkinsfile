pipeline {
    agent any

    environment {
        APP_DIR = "/var/lib/jenkins/iot-app"
        VENV_DIR = "$APP_DIR/venv"
        SCRIPT_PATH = "$APP_DIR/subscriber on AWS cloud/subscriber.py"
        LOG_FILE = "$APP_DIR/subscriber.log"
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

        stage('Copy Source Files') {
            steps {
                script {
                    sh '''
                        mkdir -p "$APP_DIR"
                        cp -r * "$APP_DIR/"
                    '''
                }
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                script {
                    sh '''
                        if [ ! -d "$VENV_DIR" ]; then
                            python3 -m venv "$VENV_DIR"
                        fi
                    '''
                }
            }
        }

        stage('Activate Virtual Env & Install Dependencies') {
            steps {
                script {
                    sh '''
                        bash -c "source '$VENV_DIR/bin/activate' && pip install --upgrade pip && pip install -r '$APP_DIR/requirements_subscriber.txt' || echo 'requirements_subscriber.txt not found, skipping...'"
                    '''
                }
            }
        }

        stage('Run EC2 Subscriber Script') {
            steps {
                script {
                    sh '''
                        nohup bash -c "source '$VENV_DIR/bin/activate' && python3 '$SCRIPT_PATH'" > "$LOG_FILE" 2>&1 &
                    '''
                }
            }
        }

        stage('Verify Installation') {
            steps {
                script {
                    sh '''
                        bash -c "source '$VENV_DIR/bin/activate' && pip list"
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
            echo "✅ Installation Successful and subscriber.py started in background!"
        }
    }
}
