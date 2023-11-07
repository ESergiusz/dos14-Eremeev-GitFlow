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
          sh 'curl -LO "curl -LO https://dl.k8s.io/release/v1.28.3/bin/linux/amd64/kubectl"'
          sh 'chmod u+x ./kubectl'
          sh './kubectl get pods'
        }
      }
    }
  }
}