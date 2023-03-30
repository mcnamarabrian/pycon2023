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
    def valid_date(payment_date):
        today = date.today()
        if payment_date < today:
            raise ValueError(f"payment_date ({payment_date}) must not be earlier than today ({today})")
        return(payment_date)

    @validator('amount')
    def valid_amount(amount):
        if 1 <= amount <= 10000:
            return(amount)
        else:
            raise ValueError(f"amount ({amount}) must be be between 1 and 10000")
