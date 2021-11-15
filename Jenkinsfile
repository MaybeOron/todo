	pipeline {

	agent any

environment {
		REGION = "eu-central-1"
		AWSPUT = "json"
		AWSID = credentials('awsid')
		REPONAME = "oron_todo"
		IMGTAG = "todo"
		INSTANCE_IP = "3.123.228.93"
	}
	
	stages {
		stage('todo - set commit msg') { 
			steps {	
				script{		
					GIT_COMMIT_MSG=sh(script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
				}
					sh """
					  echo "todo - set commit msg"
					"""	
			}
		}

			stage('todo - git - RELEASE') {
			 when {
                expression {
                    return env.BRANCH_NAME ==~ /release\/\d+\.\d+/
                }
            }       
				steps {
					sh """
					echo "git prepare release"
                    git branch --all
                    echo "~~~ on $env.BRANCH_NAME branch ~~~"				
					majorVer=\$( echo $env.BRANCH_NAME | grep -Pow [0-9]*.[0-9]* )	
                    hotfix=`git tag -l --sort=v:refname | grep \$majorVer | tail -1 | grep -ow [0-9]* | tail -1 | grep . || echo -1`
                    hotfix=\$((\$hotfix + 1))
                    git tag "\$majorVer.\$hotfix"
					"""	
			}
		}

		stage('todo - build&package - MASTER') {
			when {
                expression {
					return env.BRANCH_NAME == 'master'
                }
            }   
			steps {					
					sh """			
					echo "~~~~~~~~TODO BUILD~~~~~~~~~START"

					docker build -t todo -f Dockerfile .
					
					echo "~~~~~~~~TODO BUILD~~~~~~~~~DONE!"
					"""	
			}
			// post {
			// 	failure {
			// 		updateGitlabCommitStatus name: 'failVerify', state: 'failed'
			// 		emailext body: 'tedsearch failed.', subject: 'tedsearch pipeline results - FAILED!', to: 'oronboy100@gmail.com'
			// 	}
			// }
		}

		stage('todo - build&package - RELEASE') {
			 when {
                expression {
                    return env.BRANCH_NAME ==~ /release\/\d+\.\d+/
                }
            }    
			steps {					
					sh """			
					echo "~~~~~~~~TODO BUILD~~~~~~~~~START"

					majorVer=\$( echo $env.BRANCH_NAME | grep -Pow [0-9]*.[0-9]* )
                   	hotfix=`git tag -l --sort=v:refname | grep \$majorVer | tail -1 | grep -ow [0-9]* | tail -1 | grep . || echo -1`
                    Ver="\$majorVer.\$hotfix"

					docker build -t todo:\$Ver -f Dockerfile .
					
					echo "~~~~~~~~TODO BUILD~~~~~~~~~DONE!"
					"""	
			}
			// post {
			// 	failure {
			// 		updateGitlabCommitStatus name: 'failVerify', state: 'failed'
			// 		emailext body: 'tedsearch failed.', subject: 'tedsearch pipeline results - FAILED!', to: 'oronboy100@gmail.com'
			// 	}
			// }
		}

		stage('TODO - e2e TEST ') {
			// when {
            //     expression {
			// 		return GIT_COMMIT_MSG ==~ /.*\#e2e.*/
            //     }
            // }     
			steps {	
					sh """						
					echo "~~~~~~~~TODO E2E TEST~~~~~~~~~START~~~"				

					docker-compose up -d
					sleep 15
					curl ${INSTANCE_IP}:5000

					echo "~~~~~~~~TODO E2E TEST~~~~~~PASSED!~~~"
					"""	
			}
			post {
				always {
					sh """						
					docker-compose down
					"""	
				}
			}
		}
		stage('todo - publish to ECR - MASTER') {
			when {
                expression {
					return env.BRANCH_NAME == 'master'
                }
            }   
			steps {		            
                        withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: "aws",
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        ]]) {       
						sh """ 
						sleep 1
						aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWSID}.dkr.ecr.${REGION}.amazonaws.com
						sleep 1
						echo "pushing to ECR"
						docker tag ${IMGTAG} ${AWSID}.dkr.ecr.${REGION}.amazonaws.com/${REPONAME}:latest
						docker push ${AWSID}.dkr.ecr.${REGION}.amazonaws.com/${REPONAME}:latest
						"""	
						}
					}

			// post {
			// 	failure {
			// 		updateGitlabCommitStatus name: 'failPublish', state: 'failed'
			// 		emailext body: 'tedsearch failed.', subject: 'tedsearch pipeline results - FAILED!', to: 'oronboy100@gmail.com'
			// 	}
			// }
		}

			stage('todo - publish to ECR - RELEASE') {
			when {
                expression {
                    return env.BRANCH_NAME ==~ /release\/\d+\.\d+/
            }
            }   
			steps {		            
                        withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: "aws",
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        ]]) {       
						sh """ 

						majorVer=\$( echo $env.BRANCH_NAME | grep -Pow [0-9]*.[0-9]* )
                   		hotfix=`git tag -l --sort=v:refname | grep \$majorVer | tail -1 | grep -ow [0-9]* | tail -1 | grep . || echo -1`
                    	Ver="\$majorVer.\$hotfix"

						sleep 1
						aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWSID}.dkr.ecr.${REGION}.amazonaws.com
						sleep 1
						echo "pushing to ECR"
						docker tag ${IMGTAG}:\$Ver ${AWSID}.dkr.ecr.${REGION}.amazonaws.com/${REPONAME}:\$Ver
						docker push ${AWSID}.dkr.ecr.${REGION}.amazonaws.com/${REPONAME}:\$Ver
						"""	
						}
					}

			// post {
			// 	failure {
			// 		updateGitlabCommitStatus name: 'failPublish', state: 'failed'
			// 		emailext body: 'tedsearch failed.', subject: 'tedsearch pipeline results - FAILED!', to: 'oronboy100@gmail.com'
			// 	}
			// }
		}
		stage('todo - Clean Tag Push for releases') {
			when {
                expression {
                    return env.BRANCH_NAME ==~ /release\/\d+\.\d+/
                }
            }   
			steps {
				withCredentials([gitUsernamePassword(credentialsId: 'githubtoken', gitToolName: 'Default')]) {
					sh """ 		
					echo "~~~pushing tags~~~"
					git push --tags
					"""		
				}
			}
			// post {
			// 	failure {
			// 		updateGitlabCommitStatus name: 'build', state: 'failed'
			// 	}
			// 	success {
			// 		updateGitlabCommitStatus name: 'build', state: 'success'
			// 	}
			// }
			
		}
	}
}

