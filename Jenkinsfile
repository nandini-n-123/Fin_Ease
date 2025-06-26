

pipeline {
    agent any

    tools {
        nodejs 'NodeJS-18'  // ✅ Only NodeJS is needed
    }

    environment {
        RENDER_API_KEY      = credentials('render-api-key')
        VERCEL_TOKEN        = credentials('vercel-token')
        VERCEL_ORG_ID       = credentials('vercel-org-id')
        VERCEL_PROJECT_ID   = credentials('vercel-project-id')
        SONAR_TOKEN         = credentials('sonarcloud-token')
        GITHUB_CREDS        = credentials('github-credentials')
        RENDER_SERVICE_ID   = 'srv-d1d6ofh5pdvs73aeqit0'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                git branch: 'main', credentialsId: 'github-credentials', url: 'https://github.com/nandini-n-123/Fin_Ease.git'
            }
        }

        stage('SonarCloud Analysis') {
    steps {
        script {
           
            def scannerHome = tool name: 'sonar-scanner'

            withSonarQubeEnv('SonarCloud') {
                sh """
                    ${scannerHome}/bin/sonar-scanner \
                    -Dsonar.projectKey=nandini-n-123_Fin_Ease\
                    -Dsonar.organization=nandini-n-123 \
                    -Dsonar.sources=. \
                    -Dsonar.login=$SONAR_TOKEN
                """
            }
        }
    }
}


        stage('Wait for SonarCloud Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build and Deploy') {
            parallel {
                stage('Deploy Backend to Render') {
                    steps {
                        echo "Triggering Render deployment..."
                        sh """
                        curl -X POST \\
                          -H "Authorization: Bearer ${RENDER_API_KEY}" \\
                          -H "Accept: application/json" \\
                          -H "Content-Type: application/json" \\
                          https://api.render.com/v1/services/${RENDER_SERVICE_ID}/deploys
                        """
                    }
                }
                stage('Deploy Frontend to Vercel') {
                    steps {
                        dir('frontend') {
                            echo "Installing, Building, and Deploying Frontend..."
                            sh 'npm install'
                            sh 'npm run build'
                            sh 'npx vercel . --prod --token ${VERCEL_TOKEN} --yes'
                        }
                    }
                }
            }
        }
    }
}
