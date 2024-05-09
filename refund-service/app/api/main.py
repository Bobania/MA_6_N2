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
    {'id': 1, 'product_id': 3,   'status': 'refund_pay' },
    {'id': 2, 'product_id': 4,   'status': 'refund_pay'},
    {'id': 3, 'product_id': 5,   'status': 'not_refund_pay'}
]
# @app.get('/', tags=['Запуск'])
# async def startup():
#     await database.connect()
#     return 'База данных присоеденена'



@refunds_router.get("/get_all_refunds")
async def read_payments():
    return refund_data

@refunds_router.get("/{refunds_id}")
async def read_payment(refund_id: int):
    for refund in refund_data:
        if refund['id'] == refund_id:
            return refund
    return None



app.include_router(refunds_router, prefix='/api/refund', tags=['Refunds'])
#app.include_router(refunds, prefix='/api/refund', tags=['Refunds'])

