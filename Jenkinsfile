pipeline {
    agent any

    tools {
        // These tools must match the names you configured in Manage Jenkins > Tools
        nodejs 'NodeJS-18'
        // The SonarQube Scanner tool you configured in the UI
        sonar 'sonar-scanner' 
    }

    environment {
        // Your credentials remain the same
        RENDER_API_KEY    = credentials('render-api-key')
        VERCEL_TOKEN      = credentials('vercel-token')
        VERCEL_ORG_ID     = credentials('vercel-org-id')
        VERCEL_PROJECT_ID = credentials('vercel-project-id')
        SONAR_TOKEN       = credentials('sonarcloud-token')
        GITHUB_CREDS      = credentials('github-credentials')

        // Your Render Service ID
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
                // This 'withSonarQubeEnv' step configures the connection to your SonarCloud server
                withSonarQubeEnv('SonarCloud') {
                    // --- THIS IS THE CORRECTED AND ROBUST METHOD ---
                    script {
                        // 1. Get the installation path of the tool named 'sonar-scanner'
                        def scannerHome = tool 'sonar-scanner'
                        
                        // 2. Run the scanner command using its full, explicit path
                        // This avoids all "command not found" errors.
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
                        echo "Triggering Render deployment..."
                        sh """
                        curl -X POST \\
                          -H "Authorization: Bearer ${RENDER_API_KEY}" \\
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
                            // The vercel CLI uses the environment variables to link to the correct project
                            sh 'npx vercel --prod --token ${VERCEL_TOKEN} --yes'
                        }
                    }
                }
            }
        }
    }
}
