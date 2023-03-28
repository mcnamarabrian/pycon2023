from datetime import datetime
import random

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.parser import (
    parse,
    ValidationError
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from payment_model import Payment

tracer = Tracer()
logger = Logger()
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
    try:
        parsed_payment: Payment = parse(data, model=Payment)
    except ValidationError as e:
        logger.error(e.json())
        return {
            "error": "Invalid payment",
            "timestamp": timestamp,
        }, 400

    logger.info({
        "user_id": data['user_id'],
        "amount": data['amount'],
        "outcome": random.choice(weighted_outcomes),
        "payment_date": data['payment_date'],
        "timestamp": timestamp
    })

    return {
        "user_id": data['user_id'],
        "amount": data['amount'],
        "outcome": random.choice(weighted_outcomes),
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
