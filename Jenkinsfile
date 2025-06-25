pipeline {
    agent any

    tools {
        // We only need NodeJS here. Sonar Scanner will be handled inside its stage.
        nodejs 'NodeJS-18'
    }

    environment {
        // This securely loads the credentials you created in Jenkins
        RENDER_API_KEY  = credentials('render-api-key')
        VERCEL_TOKEN    = credentials('vercel-token')
        VERCEL_ORG_ID   = credentials('vercel-org-id')
        VERCEL_PROJECT_ID = credentials('vercel-project-id')
        SONAR_TOKEN     = credentials('sonarcloud-token')
        GITHUB_CREDS    = credentials('github-credentials')

        // Your correct Render Service ID
        RENDER_SERVICE_ID = 'srv-d1d6ofh5pdvs73aeqit0' 
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
                // This 'withSonarQubeEnv' step configures the connection to the server named 'SonarCloud'
                withSonarQubeEnv('SonarCloud') {
                    // --- THIS IS THE CORRECTED BLOCK ---
                    // 'def' is Groovy code, so it must be inside a 'script' block.
                    script {
                        // Get the installation path of the tool named 'sonar-scanner'
                        def scannerHome = tool 'sonar-scanner'
                        // Now run the scanner command using its full path
                        sh "'${scannerHome}/bin/sonar-scanner' -Dsonar.projectKey=nandini-n-123_Fin_Ease -Dsonar.organization=nandini-n-123 -Dsonar.sources=. -Dsonar.login=${SONAR_TOKEN}"
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
                        echo "Triggering Render deployment for service ID: ${RENDER_SERVICE_ID}"
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
                            echo "Installing frontend dependencies..."
                            sh 'npm install'
                            
                            echo "Building React app..."
                            sh 'npm run build'

                            echo "Deploying frontend to Vercel..."
                            sh 'npx vercel --prod --token ${VERCEL_TOKEN} --yes'
                        }
                    }
                }
            }
        }
    }
}
