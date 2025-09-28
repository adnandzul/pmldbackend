pipeline {
    agent any

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Mengambil kode dari repository...'
                checkout scm
            }
        }

        stage('2. Build Services') {
            steps {
                echo ' menyiapkan environtment variables'
                withCredentials([file(credentialsId: 'env-db-file-pmld', variable: 'ENV_DB'),
                file(credentialsId: 'env-api-file-pmld', variable: 'ENV_API')]) {
                    sh 'cp $ENV_DB .env.db'
                    sh 'cp $ENV_API .env.api'

                    echo 'Membangun image yang didefinisikan di docker-compose.yml...'
                    sh 'docker-compose build'
                }
            }
        }

        stage('3. Deploy Application') {
            steps {
                echo 'Menjalankan aplikasi dengan Docker Compose...'
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Membersihkan sisa build...'
            sh 'docker image prune -f'
        }
    }
}
