pipeline {
    agent any

    tools {
        // We only need NodeJS for the frontend build.
        // The SonarQube Scanner plugin will be found automatically by the 'withSonarQubeEnv' step.
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
                // This 'withSonarQubeEnv' step configures the connection to the server named 'SonarCloud'
                // and makes the 'sonar-scanner' command available.
                withSonarQubeEnv('SonarCloud') {
                    // This is the direct and correct way to run the scanner.
                    // It will now work because the Jenkins agent has the correct Java 17 version.
                    sh "sonar-scanner -Dsonar.projectKey=nandini-n-123_Fin_Ease -Dsonar.organization=nandini-n-123 -Dsonar.sources=. -Dsonar.login=${SONAR_TOKEN}"
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
                            // The Vercel CLI automatically uses the VERCEL_ORG_ID and VERCEL_PROJECT_ID credentials
                            sh 'npx vercel --prod --token ${VERCEL_TOKEN} --yes'
                        }
                    }
                }
            }
        }
    }
}
