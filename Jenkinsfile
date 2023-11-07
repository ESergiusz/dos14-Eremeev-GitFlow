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
        withKubeConfig([credentialsId: 'kubernetes-config']) {
          sh './kubectl get pods'
        }
      }
    }
  }
}