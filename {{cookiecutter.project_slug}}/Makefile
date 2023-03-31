BASE := $(shell /bin/pwd)
CODE_COVERAGE = 72
PIPENV ?= pipenv

target:
	$(info ${HELP_MESSAGE})
	@exit 0

.PHONY: clean
clean:
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

.PHONY: all
all: clean build

.PHONY: install
install:
	$(info [*] Installing pipenv)
	@pip install pipenv --upgrade
	$(MAKE) dev

dev:
	$(info [*] Installing pipenv project dependencies)
	@$(PIPENV) install
	@$(PIPENV) install -d

shell:
	@$(PIPENV) shell

build: ##=> Same as package except that we don't create a ZIP
	sam build --use-container --region {{ cookiecutter.aws_region }} --profile {{ cookiecutter.aws_iam_profile }}

deploy.guided: ##=> Guided deploy that is typically run for the first time only
	sam deploy --guided --region {{ cookiecutter.aws_region }} --profile {{ cookiecutter.aws_iam_profile }}

deploy: ##=> Deploy app using previously saved SAM CLI configuration
	sam deploy --region {{ cookiecutter.aws_region }} --profile {{ cookiecutter.aws_iam_profile }}

invoke-valid-get-balance: ##=> Run SAM Local function with a given event payload
	@sam local invoke GetBalanceFunction --event events/valid_get_balance.json

invoke-valid-post-payment: ##=> Run SAM Local function with a given event payload
	@sam local invoke PostPaymentFunction --event events/valid_post_payment.json

invoke-invalid-get-balance: ##=> Run SAM Local function with a given event payload
	@sam local invoke GetBalanceFunction --event events/invalid_get_balance.json

invoke-invalid-amount-post-payment: ##=> Run SAM Local function with a given event payload
	@sam local invoke PostPaymentFunction --event events/invalid_amount_post_payment.json

invoke-invalid-date-post-payment: ##=> Run SAM Local function with a given event payload
	@sam local invoke PostPaymentFunction --event events/invalid_date_post_payment.json

invoke-missing-userid-post-payment: ##=> Run SAM Local function with a given event payload
	@sam local invoke PostPaymentFunction --event events/invalid_missing_userid_post_payment.json

run: ##=> Run SAM Local API GW and can optionally run new containers connected to a defined network
	@test -z ${NETWORK} \
		&& sam local start-api \
		|| sam local start-api --docker-network ${NETWORK}

.PHONY: test
test:
	POWERTOOLS_METRICS_NAMESPACE="MyServerlessApplication" $(PIPENV) run python -m pytest --cov . --cov-report term-missing --cov-fail-under $(CODE_COVERAGE) tests/ -vv

hurry: ##=> Run full workflow for the first time
	$(MAKE) install
	$(MAKE) build
	$(MAKE) deploy.guided

#############
#  Helpers  #
#############

define HELP_MESSAGE
	Environment variables to be aware of or to hardcode depending on your use case:

	NETWORK
		Default: ""
		Info: Docker Network to connect to when running Lambda function locally

	Common usage:

	...::: Installs Pipenv, application and dev dependencies defined in Pipfile :::...
	$ make install

	...::: Builds Lambda function dependencies:::...
	$ make build

	...::: Deploy for the first time :::...
	$ make deploy.guided

	...::: Deploy subsequent changes :::...
	$ make deploy

	...::: Run SAM Local API Gateway :::...
	$ make run

	...::: Run Pytest under tests/ with pipenv :::...
	$ make test

	...::: Spawn a virtual environment shell :::...
	$ make shell

	...::: Cleans up the environment - Deletes Virtualenv, ZIP builds and Dev env :::...
	$ make clean

	Advanced usage:

	...::: Run SAM Local API Gateway within a Docker Network :::...
	$ make run NETWORK="sam-network"
endef
