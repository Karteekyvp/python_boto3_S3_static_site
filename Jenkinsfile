pipeline {
    agent any
    stages {
        stage('Deploy Static Website') {
            steps {
                sh 'python3 deploy_static_site.py'
            }
        }
    }
}

