pipeline {
    agent any

    tools {
        // These names must match what you configured in Manage Jenkins > Tools
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

        // IMPORTANT: Replace this placeholder with your actual Render Service ID
        RENDER_SERVICE_ID = 'srv-d1d6ofh5pdvs73aeqit0' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                // Use the github-credentials to checkout the code
                git branch: 'main', credentialsId: 'github-credentials', url: 'https://github.com/nandini-n-123/Fin_Ease.git'
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                withSonarQubeEnv('SonarCloud') {
                    // IMPORTANT: Replace the projectKey and organization with your values from SonarCloud
                    sh """
                    sonar-scanner \\
                      -Dsonar.projectKey=nandini-n-123_Fin_Ease \\
                      -Dsonar.organization=nandini-n-123 \\
                      -Dsonar.sources=. \\
                      -Dsonar.host.url=https://sonarcloud.io \\
                      -Dsonar.login=${SONAR_TOKEN}
                    """
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
                        // This API call tells Render to pull the latest commit and redeploy
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
                            // This command links the project using environment variables and deploys the prebuilt folder to production
                            sh 'npx vercel --prod --token ${VERCEL_TOKEN} --scope ${VERCEL_ORG_ID} --yes'
                        }
                    }
                }
            }
        }
    }
}