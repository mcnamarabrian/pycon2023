# pycon2023

This [Cookiecutter](https://github.com/cookiecutter/cookiecutter) project supports [Best Practices for Using Python to Power Serverless Applications (Sponsor: Capital One)](https://us.pycon.org/2023/schedule/presentation/152/). This session outlines lessons learned building, deploying, and operating [AWS Serverless](https://aws.amazon.com/serverless/) Python applications. Though Capital One uses AWS Lambda for many use cases, this example will create artifacts for deploying a simple HTTP API.

## Pre-requisites

* [python3.9](https://www.python.org/downloads/)

* [Pipenv](https://pipenv.pypa.io/en/latest/)

* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Usage

To get started, run the following `sam init` command and respond to the prompts.

```bash
sam init --location gh:aws-samples/mcnamarabrian/pycon2023
```

**NOTE:** Do _not_ try to clone this project directly. The rendered project will be tailored based upon your responses to several prompts.

## Developing the Project

You will need to install prerequisites to work on the project itself and not the generated artifacts.

```bash
pipenv install --dev
```

### Testing

The project makes use of the [hackebrot/pytest-cookies](https://github.com/hackebrot/pytest-cookies) project. There are unit tests that will allow you test the materialization of the template code. Tests are defined in [tests/test_render.py](./tests/test_render.py).

```bash
pipenv run pytest -v
```
