from datetime import date

from aws_lambda_powertools.utilities.parser import (
    BaseModel,
    validator
)

class Payment(BaseModel):
    user_id: str
    amount: int
    payment_date: date

    @validator('payment_date')
    def if_valid_date(payment_date):
        today = date.today()
        if payment_date < today:
            raise ValueError("payment_date must not be earlier than today")
        return(payment_date)
