import os
import random

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit


logger = Logger(utc=True)
tracer = Tracer()
metrics = Metrics()
app = ApiGatewayRestResolver()

@app.get("/get-balance/<id>")
@tracer.capture_method
def get_balance(id):
    tracer.put_annotation(key="user_id", value=id)
    logger.info({
        'user_id': id,
        'balance': random.randint(0, 10000)
    })
    metrics.add_metric(name="SuccessfulBalanceRequest", unit=MetricUnit.Count, value=1)
    return {
        'user_id': id,
        'balance': random.randint(0, 10000)
    }


@app.get("/get-balance")
@tracer.capture_method
def get_balance():
    tracer.put_annotation(key="user_id", value="unknown")
    logger.error({
        'user_id': 'unknown',
        'balance': 'unknown'
    })
    metrics.add_metric(name="UnsuccessfulBalanceRequest", unit=MetricUnit.Count, value=1)
    return {
        'user_id': 'unknown',
        'balance': 'unknown'
    }

@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST{%- if cookiecutter.production_environment == "no" %}, log_event=True{% endif %}
)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise

