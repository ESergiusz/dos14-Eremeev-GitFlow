pipeline {
  agent any
  stages {
    stage('Lint') {
      when {
        anyOf {
          branch pattern:"feature-*"
          branch pattern: "fix-*"
        }
      }
      agent {
        docker {
          image 'python:3.11.3-buster'
          args '-u 0'
        }
      }
      steps {
        sh 'pip install poetry'
        sh 'poetry install --with dev'
        sh "poetry run -- black --check *.py"
      }
    }
    stage('Build') {
      when {
        anyOf {
         branch pattern: "feature-*"
          branch pattern: "master"
        }
      }
      steps {
        script {
          def image = docker.build("esergiusz/dos14-authz:${env.GIT_COMMIT})
          customImage.push()
          customImage.push('latest')
          docker.withRegistry('','dockerhub-esa') {
            image.push()
          }
        }
      }
    }
  }
}