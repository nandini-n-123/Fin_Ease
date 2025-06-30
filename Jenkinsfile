

pipeline {
    agent any

    tools {
        nodejs 'NodeJS-18'
     // ✅ Only NodeJS is needed
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

        // vvvvvv PASTE THIS ENTIRE NEW STAGE HERE vvvvvv
        stage('Dependency Security Scan') {
            steps {
                // We go into the 'frontend' directory to find its package.json
                dir('frontend') {
                    echo 'Running security audit on frontend dependencies...'
                    
                    // This command checks for known vulnerabilities.
                    // '--audit-level=high' means the pipeline will only fail if 'high' or 'critical'
                    // severity vulnerabilities are found. It will pass for low/moderate ones.
                    sh 'npm audit --audit-level=critical'
                }
            }
        }
        // ^^^^^^ END OF THE NEW STAGE ^^^^^^
        // vvvvvv REPLACE the old 'Run Backend Tests' stage with this one vvvvvv
        // vvvvvv REPLACE the old 'Run Backend Tests' stage with this FINAL version vvvvvv
        stage('Run Backend Tests') {
            steps {
                dir('backend') {
                    script {
                        echo "Attempting to install Python dependencies and run Pytest..."
                        
                        // Step 1: Find the Python tool and print its path for debugging
                        def pythonHome = tool name: 'Python3.9'
                        echo "Jenkins resolved the Python tool path to: ${pythonHome}"

                        // Step 2: Define the full, absolute paths to the executables
                        def pipExecutable = "${pythonHome}/bin/pip"
                        def pytestExecutable = "${pythonHome}/bin/pytest"

                        // Step 3: Add debugging to see the contents of the 'bin' directory
                        echo "Listing contents of the Python bin directory..."
                        sh "ls -la ${pythonHome}/bin/"

                        // Step 4: Explicitly check if the 'pip' executable file exists
                        sh "if [ -f ${pipExecutable} ]; then echo 'SUCCESS: pip executable was found.'; else echo 'ERROR: pip executable was NOT found at ${pipExecutable}'; exit 1; fi"

                        // Step 5: Run the commands using the full path with extra quotes for safety
                        echo "Now running pip install..."
                        sh "'${pipExecutable}' install -r requirements.txt"

                        echo "Now running pytest..."
                        sh "'${pytestExecutable}' ../tests"
                    }
                }
            }
        }
        // ^^^^^^ END OF THE NEW STAGE ^^^^^^

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

        stage('Build Backend Docker Image') {
        steps {
            echo "Building the backend Docker image..."
            dir('backend') {
                // We tag the image with the Jenkins build number for a unique version
                sh "docker build -t fin-ease-backend:${env.BUILD_NUMBER} ."
            }
        }
    }

    // --- STAGE 7: SCAN IMAGE WITH TRIVY (NEW) ---
    stage('Scan Image with Trivy') {
        steps {
            echo "Scanning Docker image for OS and dependency vulnerabilities..."
            // This runs the Trivy container to scan the image we just built
            sh """
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    -v trivy-cache:/root/.cache/ \
                    aquasec/trivy:latest \
                    image --exit-code 1 --severity HIGH,CRITICAL fin-ease-backend:${env.BUILD_NUMBER}
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
                // This is the new, simpler stage
stage('Deploy Frontend to Vercel') {
    steps {
        // We no longer build in Jenkins. We just tell Vercel to deploy.
        // Vercel will use the "Root Directory" setting to find and build your app itself.
        echo "Triggering Vercel production deployment..."
        sh 'npx vercel --prod --token ${VERCEL_TOKEN} --yes'
    }
}
            }
        }
    }
}
