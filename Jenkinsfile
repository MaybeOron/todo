	pipeline {
    // tools {
	// 	// terraform 'terraform'
    // }
	agent any

environment {
		REGION = "eu-central-1"
		AWSPUT = "json"
		AWSID = credentials('awsid')
		REPONAME = "oron_todo"
		IMGTAG = "todo"
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

			stage('todo - git') {
			 when {
                expression {
                    return env.BRANCH_NAME ==~ /release\/\d+\.\d+/
                }
            }       
				steps {
					// withCredentials([gitUsernamePassword(credentialsId: 'gitcred', gitToolName: 'git-tool')]) {
					sh """				
					echo "git prepare release"
                    git branch --all
                    echo "~~~ on $env.BRANCH_NAME branch ~~~"
				
					majorVer=\$( echo $env.BRANCH_NAME | grep -Pow [0-9]*.[0-9]* )
		
                    hotfix=`git tag | grep \$majorVer | tail -1 | grep -ow [0-9]* | tail -1 | grep . || echo -1`
                    hotfix=\$((\$hotfix + 1))
                    git tag "\$majorVer.\$hotfix"
					"""	
				// }
			}
		}

		stage('todo - build&package') {
			steps {					
					sh """			
					echo "~~~~~~~~TODO BUILD~~~~~~~~~START"

					majorVer=\$( echo $env.BRANCH_NAME | grep -Pow [0-9]*.[0-9]* )
                   	hotfix=`git tag | grep \$majorVer | tail -1 | grep -ow [0-9]* | tail -1 | grep . || echo -1`
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

			

					echo "~~~~~~~~TODO E2E TEST~~~~~~PASSED!~~~"
					

					"""	
			}
			// post {
			// 	failure {
			// 		updateGitlabCommitStatus name: 'failTest', state: 'failed'
			// 		emailext body: 'tedsearch failed.', subject: 'tedsearch pipeline results - FAILED!', to: 'oronboy100@gmail.com'
			// 	}
			// }
		}

			stage('todo - publish to ECR') {
			// 	when {
            //     expression {
			// 		return GIT_COMMIT_MSG ==~ /.*\#e2e.*/
            //     }
            // }    
			steps {		            
                        withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: "aws",
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        ]]) {       
						sh """ 

						majorVer=\$( echo $env.BRANCH_NAME | grep -Pow [0-9]*.[0-9]* )
                   		hotfix=`git tag | grep \$majorVer | tail -1 | grep -ow [0-9]* | tail -1 | grep . || echo -1`
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
				// withCredentials([gitUsernamePassword(credentialsId: 'gitcred', gitToolName: 'git-tool')]) {
					sh """ 		
					echo "~~~pushing tags~~~"
					git push --tags
					"""		
				// }
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
		
		// stage('tedsearch - DEPLOY TEST ENV') {
		// 	when {
        //         expression {
		// 			return GIT_COMMIT_MSG ==~ /.*\#e2e.*/
        //         }
        //     }    
		// 	steps {       									
		// 				sshagent(['7224c2c4-8acd-4952-a193-5acd1284e9df']) {

		// 				withCredentials([[
        //                 $class: 'AmazonWebServicesCredentialsBinding',
        //                 credentialsId: "aws",
        //                 accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //                 ]]) {       
		// 				sh """ 
		// 				sleep 1
		// 				cd terraform
		// 				terraform init

		// 				lastWS=` terraform workspace list | grep test | grep -Pow [0-9]* | tail -n1 | grep . || echo "0" `
		// 				lastWS=\$((\$lastWS + 1))
						
		// 				terraform workspace new "test-\$lastWS"
		// 				terraform workspace select "test-\$lastWS"

		// 				terraform apply -var workspace_name="test-\$lastWS" -auto-approve
						
		// 				echo ~~~~~~~~~~~~~~~~~~~~~EC2_E2E_TESTS~~~~~~~~~~~~~~~~~

		// 				../e2e.sh \$(cat app_ip.txt) 90

		// 				echo ~~~~~~~~~~~~~~~~~~~~~EC2_E2E_TESTS~~~~~~~~~~~~DONE!~~~~~

		// 				### ./destroy_all_test_envs.sh  ### -> destroy all "test-[]" workspaces and their content
		// 				"""	
		// 				}				
		// 			}	
		// 	}
		// 	post {
		// 		success {
		// 			updateGitlabCommitStatus name: 'successDeploy', state: 'success'
		// 			emailext body: 'tedsearch test env successed!', subject: 'tedsearch pipeline results - PASSED!', to: 'oronboy100@gmail.com'
		// 		}
		// 		failure {
		// 			updateGitlabCommitStatus name: 'failDeploy', state: 'failed'
		// 			emailext body: 'tedsearch test env failed.', subject: 'tedsearch pipeline results - FAILED!', to: 'oronboy100@gmail.com'
		// 		}
		// 	}
		// }	
	}
}

