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
        withKubeConfig([credentialsId: 'AWS-ESA']) {
          sh './kubectl get pods'
        }
      }
    }
  }
}