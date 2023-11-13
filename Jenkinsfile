pipeline {
  agent any
  stages {
    stage('Lint') {
      when {
        anyOf {
          branch pattern: "feature-*"
          branch pattern: "develop"
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
          branch pattern: "develop"
        }
      }
      steps {
        script {
          def image = docker.build "esergiusz/dos14-authz:${env.GIT_COMMIT}"
          docker.withRegistry('','dockerhub-esa') {
            image.push()
          }
        }
      }
    }
    stage('Deploy') {
      when {
        anyOf {
          branch pattern: "master"
          branch pattern: "develop"
        }
      }
      steps {
        withKubeConfig([credentialsId: 'esa-k8s-token', serverUrl: 'https://1D740396F34543A99F12858947ABAD69.gr7.eu-west-1.eks.amazonaws.com']) {
          sh 'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3'
          sh 'chmod 700 get_helm.sh'
          sh './get_helm.sh'
          sh 'rm -rf dos14-Eremeev-GitFlow'
          sh 'git clone https://github.com/ESergiusz/dos14-Eremeev-GitFlow.git --branch master'
          sh 'helm upgrade authz-aws-prd dos14-Eremeev-GitFlow/charts/authz --values dos14-Eremeev-GitFlow/charts/authz/value.yaml -f dos14-Eremeev-GitFlow/charts/authz/env/prod.yaml --set=deployment.image.tag=$GIT_COMMIT -n ivanoff-bank'
        }
      }
    }
  }
}