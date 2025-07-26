pipeline {
    agent any
    environment {
        BLUE_PORT = '5000'
        GREEN_PORT = '5001'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Determine Inactive Environment') {
            steps {
                script {
                    def activeEnv = readFile('active_env.txt').trim()
                    env.INACTIVE_ENV = activeEnv == 'blue' ? 'green' : 'blue'
                    env.INACTIVE_PORT = env.INACTIVE_ENV == 'blue' ? env.BLUE_PORT : env.GREEN_PORT
                    echo "Inactive environment: ${env.INACTIVE_ENV} on port ${env.INACTIVE_PORT}"
                }
            }
        }
        stage('Deploy to Inactive Environment') {
            steps {
                script {
                    dir("${env.INACTIVE_ENV}") {
                        bat 'del /Q /S *.*'
                        bat 'xcopy ..\\app\\* . /E /I /Y'
                        bat 'if not exist venv (python -m venv venv)'
                        bat 'call venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                        // Write a batch file to start the app and store PID
                        writeFile file: 'start_app.bat', text: """
                            @echo off
                            set PORT=${env.INACTIVE_PORT}
                            set APP_ENV=${env.INACTIVE_ENV}
                            start /B python app.py
                            echo %PID% > app.pid
                        """
                        bat 'call start_app.bat'
                        sleep 5 // Wait for app to start
                    }
                }
            }
        }
        stage('Run Health Checks') {
            steps {
                dir('tests') {
                    bat 'python test_app.py %INACTIVE_PORT%'
                }
            }
        }
        stage('Switch Traffic') {
            steps {
                script {
                    writeFile file: 'active_env.txt', text: env.INACTIVE_ENV
                    echo "Traffic switched to ${env.INACTIVE_ENV}"
                }
            }
        }
        stage('Shutdown Old Environment') {
            steps {
                script {
                    def oldEnv = env.INACTIVE_ENV == 'blue' ? 'green' : 'blue'
                    def oldPort = oldEnv == 'blue' ? env.BLUE_PORT : env.GREEN_PORT
                    dir(oldEnv) {
                        bat script: 'if exist app.pid (for /f "tokens=*" %i in (app.pid) do taskkill /PID %i /F) || exit 0', returnStatus: true
                    }
                }
            }
        }
    }
    post {
        failure {
            script {
                echo 'Tests failed, rolling back'
                def activeEnv = readFile('active_env.txt').trim()
                def oldEnv = env.INACTIVE_ENV == 'blue' ? 'green' : 'blue'
                if (activeEnv == env.INACTIVE_ENV) {
                    writeFile file: 'active_env.txt', text: oldEnv
                    echo "Rolled back to ${oldEnv}"
                }
                dir(env.INACTIVE_ENV) {
                    bat script: 'if exist app.pid (for /f "tokens=*" %i in (app.pid) do taskkill /PID %i /F) || exit 0', returnStatus: true
                }
            }
        }
        always {
            script {
                echo 'Pipeline completed'
            }
        }
    }
}