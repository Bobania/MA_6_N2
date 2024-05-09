from fastapi import FastAPI
from refunds import refunds
from db import metadata, database, engine
from models import RefundMethod
from fastapi import FastAPI, APIRouter
import random


#metadata.create_all(engine)

app = FastAPI(title='Online store of board games: Refund', openapi_url="/refunds/openapi.json",
              docs_url="/api/refunds/docs")
#app = FastAPI(title="Интернет-магазин настольных игр 2")

# product_id = random.randint(1, 100)
# key_id = random.randint(1, 100)
# name = "s"
# status = random.choice(list(RefundMethod))
#
refunds_router = APIRouter()
refund_data = [
    {'id': 1, 'purchase_id': 3,   'status': 'refund_pay' },
    {'id': 2, 'purchase_id': 4,   'status': 'refund_pay'},
    {'id': 3, 'purchase_id': 5,   'status': 'refund_pay'}
]
# @app.get('/', tags=['Запуск'])
# async def startup():
#     await database.connect()
#     return 'База данных присоеденена'



@refunds_router.get("/get_all_payments")
async def read_refund():
    return 'Hello World'

@refunds_router.get("/{payments_id}")
async def read_payment(payment_id: int):
    for payment in refund_data:
        if payment['id'] == payment_id:
            return payment
    return None



#app.include_router(refunds_router, prefix='/api/refund', tags=['Refunds'])
app.include_router(refunds_router, prefix='/api/refund', tags=['Refunds'])

