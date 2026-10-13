pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'likithavajinepalli'
        IMAGE_NAME     = "likithavajinepalli/expense-tracker"
    }

    stages
    {
        stage('Checkout Code') {
            steps {
                echo "Pulling latest code from Git"
                checkout scm
            }
        }
        stage('Selenium Tests with pytest'){
            steps{
                echo "Running Selenium Tests with pytest"
                bat 'pip install -r requirements.txt'
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat 'python -m pytest -v test_expense.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"
                bat "docker build -t expense-tracker:latest ."
            }
        }
        stage('Docker Login') {
            steps {
                echo "Logging in to Docker Hub..."
                bat "docker login -u likithavajinepalli -p Likkibala@L?1010"
                }
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Pushing Docker Image to Docker Hub..."
                bat "docker push likithavajinepalli/expense-tracker:latest"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes..."
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
            
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully! App'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
