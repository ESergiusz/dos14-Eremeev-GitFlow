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
        sh "kubectl set image deployment.v1.apps/authz authz=esergiusz/dos14-authz:e1f869db8b0fde2f9ba61887b18a202e82c4d409 -n ivanoff-bank"
      }
    }
  }
}