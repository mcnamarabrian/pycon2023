import json

from src.get_balance import app


def test_valid_get_balance(valid_get_balance_event, lambda_context):
    ret = app.lambda_handler(valid_get_balance_event, lambda_context)
    # Only including user_id since the balance and timestamp
    # are non-deterministic.
    expected = {"user_id": "b0479af6-0744-4d4f-91af-c7731a5f33e2"}
    ret_body = json.loads(ret['body'])
    ret_user_id = ret_body['user_id']
    assert ret["statusCode"] == 200
    assert ret_user_id == expected['user_id']


def test_invalid_get_balance(invalid_get_balance_event, lambda_context):
    ret = app.lambda_handler(invalid_get_balance_event, lambda_context)
    expected_body = "I'm a teapot!"
    assert ret["statusCode"] == 418
    assert ret["body"] == expected_body
