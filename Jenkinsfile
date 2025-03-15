pipeline {
    agent any
    stages {
        stage('Check Python Environment') {
            steps {
                sh '''
                    which python3
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install boto3  # Explicitly install boto3 inside venv
                    python3 -c "import boto3; print(boto3.__version__)"  # Verify installation
                '''
            }
        }
        stage('Deploy Static Website') {
            steps {
                sh '''
                    source venv/bin/activate
                    python deploy_static_site.py
                '''
            }
        }
    }
}
