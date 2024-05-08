import enum
from pydantic import BaseModel
from typing_extensions import List, Optional


class RefundMethod(enum.Enum):
    PAY = 'refund_pay'
    NOT_PAY = 'not_refund_pay'


class RefundStatuses(enum.Enum):
    REFUND_GAME = 'refund_game'
    NOT_REFUND_GAME = 'not_refund_game'


class RefundIn(BaseModel):
    product_id: int
    status: RefundMethod


class RefundOut(RefundIn):
    id: int



