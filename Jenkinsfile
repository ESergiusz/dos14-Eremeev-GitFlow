pipeline {
  agent any
  stages {
    stage('Deploy') {
      when {
        anyOf {
          branch pattern: "feature-*"
        }
      }
      steps {
        withKubeConfig([serverUrl: 'https://1D740396F34543A99F12858947ABAD69.gr7.eu-west-1.eks.amazonaws.com']) {
          sh './kubectl get pods'
        }
      }
    }
  }
}