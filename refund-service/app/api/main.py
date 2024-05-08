from fastapi import FastAPI
from refunds import refunds
from db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(title="Интернет-магазин настольных игр 2")

@app.get('/', tags=['Запуск'])
async def startup():
    await database.connect()
    return 'База данных присоеденена'


app.include_router(refunds, prefix='/api/refund', tags=['Refunds'])

