# {{ cookiecutter.project_name }}

This project contains a [AWS serverless application](https://aws.amazon.com/serverless) - a representative Application Programming Interface (API) that allows users to get balance information and post payments. It includes best practices for developing, deploying, and observing serverless applications.

![PyCon-LogicalArchitecture](https://user-images.githubusercontent.com/17259/230391371-8b490174-24a2-4649-9572-230f182ea569.png)

## Dependencies

The sample application uses the Serverless Application Model to build and deploy. requires the following dependencies:

* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

* [Python3.9](https://www.python.org/downloads/release/python-390/)

* [Pipenv](https://pipenv.pypa.io/en/latest/)

* Optional: [Docker Desktop](https://www.docker.com/products/docker-desktop/) if deploying and testing locally

## Installing Python Dependencies

The local testing environment makes use of dependencies in the project's [Pipfile](./Pipfile). These dependencies need to be installed by running the following command:

```bash
pipenv install --dev
```

## What's Next?

Now that you have your project dependencies installed, you can [build and interact with the API locally](./README-INTERACTING-LOCALLY.md).
