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
                bat '''
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                '''
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

        stage('Static Analysis') {
            steps {
                bat 'coverage run -m pytest'
                bat 'coverage report --fail-under=70'
                bat 'pylint logic data app.py'
                bat 'bandit -r app.py logic data'
            }
        }

        stage('Functional Tests') {
            steps {
                bat '''
                    start /B streamlit run app.py
                    timeout /t 10
                    python -m pytest tests/test_functional.py
                '''
            }
        }

        

        stage('Deploy') {
            steps {
                bat 'ansible-playbook deployment/deploy.yml'
            }
        }
    }
}