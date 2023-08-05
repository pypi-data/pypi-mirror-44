pipeline {
    agent any

    environment {
        COMMIT_MESSAGE = """${sh(
            returnStdout: true,
            script: "git --no-pager log --format='medium' -1 ${GIT_COMMIT}"
        )}"""
        COMMIT_HASH = """${sh(
            returnStdout: true,
            script: "git describe --always"
        )}"""

        PYTHON_VERSION = '3.7.2'

        PYPIRC_CREDENTIALS = "pypirc-kaden-vt"

        DOCKER_REPO = "kadenlnelson/realvalidation"
        DOCKER_CREDENTIALS = "docker-hub-kadenlnelson"
    }

    stages {
        stage('Notify Slack') {
            steps {
                slackSend(color: '#000000', message: "Build Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)\n```${env.COMMIT_MESSAGE}```")
            }
        }

        stage('Build & Push Python Distributions') {
            agent { docker { image "python:${PYTHON_VERSION}" } }
            steps {
              sh 'pip install -r requirements.txt'
              sh 'rm -rf dist'
              sh 'python setup.py sdist bdist_wheel'
              script {
                SEMVER = """${sh(
                    returnStdout: true,
                    script: "python setup.py --version"
                )}"""
              }
              withCredentials([file(credentialsId: "${PYPIRC_CREDENTIALS}", variable: 'PYPIRC')]) {
                  sh 'twine upload --config-file $PYPIRC dist/*'
              }
              slackSend (color: '#ffde57', message: "PyPi Package Pushed - https://pypi.org/project/realvalidation/\n```\nTry it out!\n\npip install realvalidation==${SEMVER}```")
            }
        }

		    stage('Build & Push Docker Image') {
            agent { docker { image 'docker:18.09.2' } }
            steps {
                script {
                    def branchName = "${GIT_BRANCH}".replace('/', '_')
                    def image = docker.build("${DOCKER_REPO}")

                    docker.withRegistry('', "${DOCKER_CREDENTIALS}") {
                        image.push(branchName)
                        image.push("${SEMVER}")
                    }
                }

                slackSend (color: '#0db7ed', message: "Docker Image Built & Pushed - https://hub.docker.com/r/kadenlnelson/realvalidation/tags\n```\nTry it out!\n\ndocker run --rm ${DOCKER_REPO}:${SEMVER}```")
            }
        }
    }

    post {
        failure {
            slackSend (color: '#FF0000', message: "Build Failed! - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }

        success {
            slackSend (color: '#00FF00', message: "Success! - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }
    }
}
