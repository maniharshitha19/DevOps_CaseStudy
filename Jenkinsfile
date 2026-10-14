pipeline {
    agent any

    environment {
        IMAGE_NAME = "expense-tracker"
        IMAGE_TAG  = "latest"
        REPO_NAME  = "a2casestudy"
        USER_NAME  = "likithavajinepalli"
        DOCKERHUB_IMAGE = "likithavajinepalli/a2casestudy:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Pulling latest code from Git"
                checkout scm
            }
        }

        stage('Selenium Tests with pytest') {
            steps {
                echo "Running Selenium Tests with pytest"
                bat 'pip install -r requirements.txt'
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat 'python -m pytest -v test_expense.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image expense-tracker:latest"
                bat "docker build -t expense-tracker:latest ."
            }
        }

        stage('Tag Docker Image') {
            steps {
                echo "Tagging expense-tracker:latest as likithavajinepalli/a2casestudy:latest"
                bat "docker tag expense-tracker:latest likithavajinepalli/a2casestudy:latest"
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging in to Docker Hub..."
                bat 'docker login -u likithavajinepalli -p Likkibala@L?1010'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Pushing likithavajinepalli/a2casestudy:latest to Docker Hub..."
                bat "docker push likithavajinepalli/a2casestudy:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes..."
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
                bat "kubectl rollout restart deployment/expense-tracker-deployment"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Deployed likithavajinepalli/a2casestudy:latest"
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}