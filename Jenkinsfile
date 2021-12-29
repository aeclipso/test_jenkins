pipeline {
    agent any

    stages {
        stage('clone') {
            steps {
                git branch: 'release/v8.2.0', url: 'https://github.com/WebGoat/WebGoat.git'
                echo "COMPLETE CLONE"
            }
        }
        stage('build') {
            agent { docker 'maven:3.8.2-adoptopenjdk-15' }
            steps{
                echo "THIS IS BUILD START"
                echo 'Hello, Maven'
                sh 'mvn --version'
                sh 'mvn clean install -Dmaven.test.skip.exec'
                echo "THIS IS BUILD END"
            }
        }
        stage('SAST') {
            when {
                expression { params.SAST == true }
            }
            steps{
                echo "SAST"
                script{
                try {
                    sh '/usr/sbin/findsecbugs webgoat-server ./webgoat-server/target/webgoat-server-8.2.0.jar'
                }
                catch (err) {
                    echo "Error" + err.toString()
                    currentBuild.result = 'UNSTABLE'
                }
                echo "SAST END"
                }
            }
        }
        
        stage ('OSS') {
            steps {
            echo "OSS"
                script{
                    sh 'pwd'
                    try {
                        sh '/usr/sbin/dependency-check --out . --scan  ./webgoat-server/target/webgoat-server-8.2.0.jar '
                    } catch (err) {
                        echo "Error" + err.toString()
                        currentBuild.result = 'UNSTABLE'
                    }
                    echo "OSS END"
                }
            }
        }
        stage ('get logs'){
            steps{
                echo "LOGS"
                script{
                sh 'cp /var/lib/jenkins/workspace/f_pipe/dependency-check-report.html /tmp/logs/'
                }
            }
        }
    }
    post {
        always {
            script {
                echo "Clean"
                
                cleanWs notFailBuild: true
            }
        }
    } 
}
