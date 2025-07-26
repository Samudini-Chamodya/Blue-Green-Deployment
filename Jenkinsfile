pipeline {
    agent any
    environment {
        GREEN_PORT = '5001'
        BLUE_PORT = '5000'
        ACTIVE_ENV = 'blue'
    }
    stages {
        stage('Setup Green Environment') {
            steps {
                script {
                    dir('green') {
                        // Copy application files
                        bat 'xcopy ..\\app\\* . /E /I /Y'
                        
                        // Ensure Python is available and create virtual environment
                        bat '''
                            where python
                            python --version
                            if not exist venv (
                                python -m venv venv
                                if errorlevel 1 (
                                    echo Failed to create virtual environment
                                    exit /b 1
                                )
                            )
                            if exist venv\\Scripts\\activate.bat (
                                call venv\\Scripts\\activate.bat
                                pip install --no-cache-dir -r requirements.txt
                            ) else (
                                echo Virtual environment activation script not found
                                exit /b 1
                            )
                        '''
                    }
                }
            }
        }
        stage('Run Health Checks') {
            steps {
                dir('tests') {
                    bat "python test_app.py ${GREEN_PORT}"
                }
            }
        }
        stage('Switch Traffic') {
            steps {
                script {
                    bat "python traffic_router.py ${GREEN_PORT}"
                    env.ACTIVE_ENV = 'green'
                }
            }
        }
        stage('Shutdown Old Environment') {
            steps {
                dir('blue') {
                    bat '''
                        if exist app.pid (
                            for /f "tokens=*" %%i in (app.pid) do (
                                taskkill /PID %%i /F
                            )
                            del app.pid
                        )
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed'
        }
        failure {
            echo 'Tests failed, rolling back'
            script {
                dir("${env.ACTIVE_ENV}") {
                    bat '''
                        if exist app.pid (
                            for /f "tokens=*" %%i in (app.pid) do (
                                taskkill /PID %%i /F
                            )
                            del app.pid
                        )
                    '''
                }
            }
        }
    }
}