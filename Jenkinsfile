pipeline {
    agent any

    tools {
        // We only need to define NodeJS here, as Sonar Scanner will be handled inside its stage.
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
                    // This 'tool' step finds the SonarQube Scanner you configured with the name 'sonar-scanner'
                    // and gets its installation path.
                    def scannerHome = tool name: 'sonar-scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'

                    // We now run the scanner command by providing its full path and passing the login token securely
                    // This is the most reliable way and avoids PATH issues.
                    sh "'${scannerHome}/bin/sonar-scanner' -Dsonar.projectKey=nandini-n-123_Fin_Ease -Dsonar.organization=nandini-n-123 -Dsonar.sources=. -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('Wait for SonarCloud Quality Gate') {
            steps {
                // This stage waits for the analysis to complete on SonarCloud's side
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
