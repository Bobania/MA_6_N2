from products import products
from db import metadata, database, engine
from fastapi import FastAPI

metadata.create_all(engine)

app = FastAPI(title="Интернет-магазин настольных игр")


@app.get("/", tags=['Запуск'])
async def startup():
    await database.connect()
    return 'Успех!'


app.include_router(products, prefix='/api/products', tags=['Склад'])

