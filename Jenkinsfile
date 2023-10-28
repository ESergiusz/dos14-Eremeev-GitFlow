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
          branch pattern: "master"
          branch pattern:"feature-*"
          }
      }
      steps {
        script {
          def image = docker.build "esergiusz/dos14-authz:${env.GIT_COMMIT}"
          docker.withRegistry('','dockerhub-esa') {
            image.push()
            image.push('latest')
          }
        }
      }
    }
    stage('Deploy') {
      when {
        anyOf {
          branch pattern: "master"
                  }
      }
      steps {
        sh 'kubectl set image deployment.v1.apps/authz authz=esergiusz/dos14-authz:${env.GIT_COMMIT} -n ivanoff-bank'
      }
    }
  }
}