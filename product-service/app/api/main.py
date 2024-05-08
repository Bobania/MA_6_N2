from fastapi import FastAPI
from products import products
from db import metadata, database, engine

# main лежит тут потому что иначе не работают функции в __init__.py (Он не пустой)
# НЕ ЗАБУДЬТЕ СДЕЛАТЬ pip freeze > requirements.txt ИМЕННО В ТОЙ ДИРЕКТОРИИ ГДЕ ЛЕЖИТ МИКРОСЕРВИС:
# cd payment-service и cd purchse-service (Назад cd ..)

# Моя ошибка при docker compose up --build:
# payment_service-1   | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "127.0.0.1", port 5432 failed: Connection refused
# payment_service-1   |   Is the server running on that host and accepting TCP/IP connections?

metadata.create_all(engine)

app = FastAPI(title="Интернет-магазин настольных игр")


async def startup():
    await database.connect()
    return 'Database connected'

@app.on_event("startup")
async def startup_event():
    await startup()


app.include_router(products, prefix='/api/products', tags=['Склад'])
