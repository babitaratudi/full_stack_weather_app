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
        sh 'docker build -t weather-app .'
      }
    }

    stage('Trigger Render Deploy') {
      steps {
        sh 'curl -X POST "$RENDER_DEPLOY_HOOK_URL"'
      }
    }
  }
}