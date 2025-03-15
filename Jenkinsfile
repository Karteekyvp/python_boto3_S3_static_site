pipeline {
    agent any
    stages {
        stage('Check Python Environment') {
            steps {
                sh '''
                    which python3
                    python3 -m venv venv
                    source venv/bin/activate
                    python3 -c "import boto3; print(boto3.__version__)"
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
