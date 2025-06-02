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
        bat 'docker build -t weather-app .'
      }
    }

    stage('Trigger Render Deploy') {
      steps {
        bat 'curl -X POST "$RENDER_DEPLOY_HOOK_URL"'
      }
    }
  }
}