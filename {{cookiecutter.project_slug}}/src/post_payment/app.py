from datetime import datetime
import random

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import (
    parse,
    ValidationError
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from payment_model import Payment

logger = Logger()
metrics = Metrics()
tracer = Tracer()
app = APIGatewayRestResolver()

# Create a list of weighted outcomes - 90% of them will be success, 10% failure
payment_outcomes = ['success', 'failure']
weighted_outcomes = random.choices(
    payment_outcomes, cum_weights=(90, 10),
    k=100
)


@app.post("/payment")
@tracer.capture_method
def post_payment() -> dict:
    data: dict = app.current_event.json_body
    timestamp = datetime.now().isoformat()
    payment_outcome = random.choice(weighted_outcomes)
    try:
        parse(data, model=Payment)
    except ValidationError as e:
        logger.error(e.json())
        return {
            "error": "Invalid payment",
            "timestamp": timestamp,
        }, 400

    logger.info({
        "user_id": data['user_id'],
        "amount": data['amount'],
        "outcome": payment_outcome,
        "payment_date": data['payment_date'],
        "timestamp": timestamp
    })
    tracer.put_annotation(key='user_id', value=data['user_id'])

    if payment_outcome == 'success':
        metrics.add_metric(name="SuccessfulPayment", unit=MetricUnit.Count, value=data['amount'])
    else:
        metrics.add_metric(name="UnsuccessfulPayment", unit=MetricUnit.Count, value=data['amount'])

    return {
        "user_id": data['user_id'],
        "amount": data['amount'],
        "outcome": payment_outcome,
        "payment_date": data['payment_date'],
        "timestamp": timestamp
    }, 200
    
# You can continue to use other utilities just as before
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST{%- if cookiecutter.production_environment == "no" %},
    log_event=True{% endif %}
)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
