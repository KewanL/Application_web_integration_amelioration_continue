pipeline {
agent any

```
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

    stage('Static Analysis') {
        steps {
            bat """
                coverage run -m pytest tests/test_services.py tests/test_integration.py
                coverage report --fail-under=70
                pylint logic data app.py
                bandit -r app.py logic data
            """
        }
    }

    stage('Functional Tests') {
        steps {
            bat """
                start /B streamlit run app.py --server.headless true
                timeout /t 15
                python -m pytest tests/test_functional.py
            """
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
        bat 'taskkill /F /IM streamlit.exe >nul 2>&1 || exit 0'
        bat 'taskkill /F /IM python.exe >nul 2>&1 || exit 0'
    }
}
```

}
