pipeline {
    agent any

    environment {
        SNYK_TOKEN   = credentials('SNYK_TOKEN')      // Secret Text credential
        DOCKER_CREDS = credentials('dockercred')      // Username + Password
        DOCKER_IMAGE = 'jeevan725/pygame'
        DOCKER_TAG   = "v${env.BUILD_NUMBER}"         // Dynamic tag per build
        PATH         = "/usr/local/bin:${env.PATH}"   // Ensure helm, kind, docker are found
        KUBECONFIG   = '/home/jenkins/.kube/config'   // Point to your kubeconfig
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Jeevanfrankline1988/Project.git'
            }
        }

        stage('Setup Python venv & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Python Game (Headless)') {
            steps {
                sh '''
                    . venv/bin/activate
                    python sgame.py || true   # don't fail build if pygame needs GUI
                '''
            }
        }
              
        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest
                    pytest --maxfail=1 --disable-warnings -q tests/ || true
                '''
            }
        }

        stage('Snyk Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    snyk test --all-projects || true 
                '''
            }
        }

             stage('SonarQube Scan') {
               steps {
                withSonarQubeEnv('SonarScanner') {
                    sh "${tool 'SonarScanner'}/bin/sonar-scanner"
                }
            }
        } 

      stage('Quality Gate') {
          steps {
              script {
               timeout(time: 10, unit: 'MINUTES') {
                 waitForQualityGate abortPipeline: true
               }
             }
          }
        }

          stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_IMAGE:$DOCKER_TAG -t $DOCKER_IMAGE:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin
                docker push $DOCKER_IMAGE:$DOCKER_TAG
                docker push $DOCKER_IMAGE:latest
                """
            }
        }    
        stage('Deploy with Helm') {
            steps {
                sh '''
                helm upgrade --install pygame ./helm-chart \
                  --set image.repository=jeevan725/pygame \
                  --set image.tag=$DOCKER_TAG
                '''
            }
        }
              stage('Update Helm Values for ArgoCD') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-pat', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        sed -i "s|tag:.*|tag: \\"$DOCKER_TAG\\"|g" helm-chart/values.yaml
                        
                        git config user.email "jenkins@ci.local"
                        git config user.name "Jenkins CI"

                        git remote set-url origin https://${GIT_USER}:${GIT_TOKEN}@github.com/Jeevanfrankline1988/Project.git

                        git add helm-chart/values.yaml
                        git commit -m "Update image tag to $DOCKER_TAG [ci skip]" || true
                        git push origin main
                    '''
                }
            }
        }
    }      
