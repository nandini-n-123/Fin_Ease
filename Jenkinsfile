pipeline {
    agent any

    tools {
        nodejs 'NodeJS-18'
    }

    environment {
        RENDER_API_KEY    = credentials('render-api-key')
        VERCEL_TOKEN      = credentials('vercel-token')
        VERCEL_ORG_ID     = credentials('vercel-org-id')
        VERCEL_PROJECT_ID = credentials('vercel-project-id')
        SONAR_TOKEN       = credentials('sonarcloud-token')
        GITHUB_CREDS      = credentials('github-credentials')
        RENDER_SERVICE_ID = 'srv-d1d6ofh5pdvs73aeqit0'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                git branch: 'main', credentialsId: 'github-credentials', url: 'https://github.com/nandini-n-123/Fin_Ease.git'
            }
        }

        stage('Dependency Security Scan') {
            steps {
                dir('frontend') {
                    echo 'Running security audit on frontend dependencies...'
                    sh 'npm audit --audit-level=critical'
                }
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                script {
                    def scannerHome = tool name: 'sonar-scanner'
                    // This direct command is more reliable and prevents the pipeline from hanging.
                    sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=nandini-n-123_Fin_Ease \
                        -Dsonar.organization=nandini-n-123 \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=https://sonarcloud.io \
                        -Dsonar.token=${SONAR_TOKEN}
                    """
                }
            }
        }

        // vvvvvv THIS IS THE CORRECTED STAGE vvvvvv
        stage('Wait for SonarCloud Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    // By wrapping only this step, it can find the analysis report
                    // left behind by the previous stage.
                    withSonarQubeEnv('SonarCloud') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        // ^^^^^^ END OF THE CORRECTED STAGE ^^^^^^

        stage('Scan Filesystem with Trivy') {
            steps {
                echo "Scanning project filesystem for vulnerabilities..."
                sh """
                    docker run --rm -v ${env.WORKSPACE}:/scan-target \
                        -v trivy-cache:/root/.cache/ \
                        aquasec/trivy:latest \
                        fs --exit-code 1 --severity HIGH,CRITICAL /scan-target
                """
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
                        echo "Triggering Vercel production deployment..."
                        sh 'npx vercel --prod --token ${VERCEL_TOKEN} --yes'
                    }
                }
            }
        }
    }
}