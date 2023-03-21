import json
from uuid import uuid4

import pytest


class MockContext(object):
    def __init__(self, function_name):
        self.function_name = function_name
        self.function_version = "$LATEST"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = (
            f"arn:aws:lambda:us-east-1:0123456789012:function:{self.function_name}"
        )
        self.aws_request_id = str(uuid4)


@pytest.fixture
def lambda_context():
    return MockContext("awesome_function")


@pytest.fixture()
def apigw_get_balance_event():
    """Generates API GW Event"""
    with open("../events/get_balance.json", "r") as fp:
        return json.load(fp)


@pytest.fixture()
def apigw_post_payment_event():
    """Generates API GW Event"""
    with open("../events/post_payment.json", "r") as fp:
        return json.load(fp)
