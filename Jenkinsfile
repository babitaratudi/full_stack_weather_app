pipeline {
  agent any

  environment {
    RENDER_DEPLOY_HOOK_URL = credentials('RENDER_DEPLOY_HOOK_URL')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        timeout(time: 30, unit: 'MINUTES') { // Set timeout for this stage
          bat 'docker build -t weather-app .'
        }
      }
    }

    stage('Trigger Render Deploy') {
      steps {
        bat 'curl -X POST "%RENDER_DEPLOY_HOOK_URL%"'
      }
    }
  }
}