pipeline {
    agent any
    stages {
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