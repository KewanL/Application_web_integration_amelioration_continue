pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                bat 'echo Build successful'
            }
        }

        stage('Install dependencies') {
            steps {
                bat """
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                """
            }
        }

        stage('Unit Tests') {
            steps {
                bat 'python -m pytest tests/test_services.py'
            }
        }

        stage('Integration Tests') {
            steps {
                bat 'python -m pytest tests/test_integration.py'
            }
        }

        stage('Start Application') {
            steps {
                bat '''
                start "" cmd /c "python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true"
                '''
                bat 'ping 127.0.0.1 -n 30 > nul'
                bat 'curl http://127.0.0.1:8501'
            }
        }

        stage('Functional Tests') {
            steps {
                bat 'python -m pytest tests/test_functional.py'
            }
        }

        stage('Static Analysis') {
            steps {
                bat 'coverage run -m pytest tests/test_services.py tests/test_integration.py'
                bat 'coverage report --fail-under=70'
                bat 'pylint logic data app.py'
                bat 'bandit -r app.py logic data'
            }
        }

        stage('Deploy') {
            steps {
                bat 'ansible-playbook deployment/deploy.yml'
            }
        }
    }

    post {
        always {
            bat 'taskkill /F /IM python.exe || exit 0'
        }
    }
}