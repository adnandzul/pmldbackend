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
                echo 'Membangun image untuk layanan yang didefinisikan di docker-compose.yml...'
                sh 'docker-compose build'
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
