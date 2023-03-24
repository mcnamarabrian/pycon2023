from datetime import datetime
import random

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
)
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@app.get("/balance/<user_id>")
@tracer.capture_method
def get_balance(user_id: str) -> dict:
    balance = random.randint(0, 10000)
    current_timestamp = datetime.now()
    logger.info({
        "user_id": user_id,
        "balance": balance,
        "timestamp": current_timestamp.isoformat()
    })

    return {
        "user_id": user_id,
        "balance": balance,
        "timestamp": current_timestamp.isoformat()
    }


@app.not_found
@tracer.capture_method
def handle_not_found_errors(exc: NotFoundError) -> Response:
    logger.info(f"Not found route: {app.current_event.path}")
    return Response(status_code=418, content_type=content_types.TEXT_PLAIN, body="I'm a teapot!")

# You can continue to use other utilities just as before
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST{%- if cookiecutter.production_environment == "no" %}, log_event=True{% endif %}
)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
