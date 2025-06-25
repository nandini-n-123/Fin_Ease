pipeline {
    agent any

    tools {
        // --- FIXED THIS BLOCK ---
        // These names must match what you configured in Manage Jenkins > Tools
        nodejs 'NodeJS-18'
        // This tells Jenkins to find the SonarQube Scanner tool you named 'sonar-scanner'
        sonar 'sonar-scanner'
    }

    environment {
        // This securely loads the credentials you created in Jenkins
        RENDER_API_KEY  = credentials('render-api-key')
        VERCEL_TOKEN    = credentials('vercel-token')
        VERCEL_ORG_ID   = credentials('vercel-org-id')
        VERCEL_PROJECT_ID = credentials('vercel-project-id')
        SONAR_TOKEN     = credentials('sonarcloud-token')
        GITHUB_CREDS    = credentials('github-credentials')

        // This is your correct Render Service ID
        RENDER_SERVICE_ID = 'srv-d1d6ofh5pdvs73aeqit0' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                // This stage was already correct
                git branch: 'main', credentialsId: 'github-credentials', url: 'https://github.com/nandini-n-123/Fin_Ease.git'
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                // --- FIXED THIS STAGE ---
                // This is a more robust way to run the scanner that avoids PATH issues
                // and securely passes the token.
                withSonarQubeEnv('SonarCloud') {
                    script {
                        // This 'scannerHome' variable is provided by the 'tools' block above
                        def scannerHome = tool 'sonar-scanner'
                        // We explicitly add the scanner to the system's PATH
                        // and pass the token securely as an environment variable
                        withEnv(["PATH+SCANNER=${scannerHome}/bin", "SONAR_LOGIN=${SONAR_TOKEN}"]) {
                            sh """
                            sonar-scanner \\
                              -Dsonar.projectKey=nandini-n-123_Fin_Ease \\
                              -Dsonar.organization=nandini-n-123 \\
                              -Dsonar.sources=. \\
                              -Dsonar.host.url=https://sonarcloud.io \\
                              -Dsonar.login=${SONAR_LOGIN}
                            """
                        }
                    }
                }
            }
        }

        stage('Wait for SonarCloud Quality Gate') {
            steps {
                // This stage was already correct
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build and Deploy') {
            parallel {
                stage('Deploy Backend to Render') {
                    steps {
                        // This stage was already correct
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
                        // This stage was already correct
                        dir('frontend') {
                            echo "Installing frontend dependencies..."
                            sh 'npm install'
                            
                            echo "Building React app..."
                            sh 'npm run build'

                            echo "Deploying frontend to Vercel..."
                            // The vercel CLI uses the VERCEL_ORG_ID and VERCEL_PROJECT_ID
                            // environment variables to link to the correct project automatically.
                            sh 'npx vercel --prod --token ${VERCEL_TOKEN} --yes'
                        }
                    }
                }
            }
        }
    }
}
