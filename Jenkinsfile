pipeline {
    agent any
    environment {
        GREEN_PORT = '5001'
        BLUE_PORT = '5000'
        ACTIVE_ENV = 'blue'
        PYTHON_EXEC = 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Debug Workspace') {
            steps {
                // List workspace contents to verify repository structure
                bat 'dir /S'
            }
        }
        stage('Setup Green Environment') {
            steps {
                script {
                    dir('green') {
                        // Try copying from app directory first
                        bat '''
                            if exist ..\\app (
                                echo Copying from app directory
                                xcopy ..\\app\\* . /E /I /Y
                            ) else (
                                echo app directory not found, copying from root
                                xcopy ..\\* . /E /I /Y /EXCLUDE:exclude.txt
                                echo templates > exclude.txt
                                echo blue >> exclude.txt
                                echo green >> exclude.txt
                                echo tests >> exclude.txt
                            )
                            dir
                        '''
                        
                        // Debug Python environment and create virtual environment
                        bat '''
                            echo Python executable: %PYTHON_EXEC%
                            "%PYTHON_EXEC%" --version
                            if not exist venv (
                                "%PYTHON_EXEC%" -m venv venv
                                if errorlevel 1 (
                                    echo Failed to create virtual environment
                                    exit /b 1
                                )
                                dir venv\\Scripts
                            ) else (
                                echo Virtual environment already exists, removing and recreating
                                rmdir /S /Q venv
                                "%PYTHON_EXEC%" -m venv venv
                                if errorlevel 1 (
                                    echo Failed to create virtual environment
                                    exit /b 1
                                )
                                dir venv\\Scripts
                            )
                            if exist venv\\Scripts\\activate.bat (
                                call venv\\Scripts\\activate.bat
                                pip install --no-cache-dir -r requirements.txt
                            ) else (
                                echo Virtual environment activation script not found
                                dir venv
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
                    bat '"%PYTHON_EXEC%" test_app.py %GREEN_PORT%'
                }
            }
        }
        stage('Switch Traffic') {
            steps {
                script {
                    bat '"%PYTHON_EXEC%" traffic_router.py %GREEN_PORT%'
                    env.ACTIVE_ENV = 'green'
                }
            }
        }
        stage('Shutdown Old Environment') {
            steps {
                dir('blue') {
                    bat '''
                        if exist app.pid (
                            for /F "tokens=*" %%i in (app.pid) do (
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
                            for /F "tokens=*" %%i in (app.pid) do (
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