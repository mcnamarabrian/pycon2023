import json

from src.post_payment import app


def test_valid_post_payment(valid_post_payment_event, lambda_context):
    ret = app.lambda_handler(valid_post_payment_event, lambda_context)
    # Only including user_id, amount, and payment_date since the 
    # outcome and timestamp are non-deterministic.
    expected = {"user_id":"brian","amount":1000, "payment_date":"2100-05-01"}
    ret_body = json.loads(ret['body'])
    ret_user_id = ret_body['user_id']
    ret_amount = ret_body['amount']
    ret_payment_date = ret_body['payment_date']
    assert ret["statusCode"] == 200
    assert ret_user_id == expected['user_id']
    assert ret_amount == expected['amount']
    assert ret_payment_date == expected['payment_date']


def test_invalid_amount_post_payment(invalid_amount_post_payment_event, lambda_context):
    ret = app.lambda_handler(invalid_amount_post_payment_event, lambda_context)
    # Only including error since the timestamp is non-deterministic.
    expected = {"error":"Invalid payment"}
    ret_body = json.loads(ret['body'])
    ret_error = ret_body['error']
    assert ret["statusCode"] == 400
    assert ret_error == expected['error']

def test_invalid_date_post_payment(invalid_date_post_payment_event, lambda_context):
    ret = app.lambda_handler(invalid_date_post_payment_event, lambda_context)
    # Only including error since the timestamp is non-deterministic.
    expected = {"error":"Invalid payment"}
    ret_body = json.loads(ret['body'])
    ret_error = ret_body['error']
    assert ret["statusCode"] == 400
    assert ret_error == expected['error']

def test_invalid_missing_userid_post_payment(invalid_missing_userid_post_payment_event, lambda_context):
    ret = app.lambda_handler(invalid_missing_userid_post_payment_event, lambda_context)
    # Only including error since the timestamp is non-deterministic.
    expected = {"error":"Invalid payment"}
    ret_body = json.loads(ret['body'])
    ret_error = ret_body['error']
    assert ret["statusCode"] == 400
    assert ret_error == expected['error']
