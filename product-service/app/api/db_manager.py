from fastapi import HTTPException

from models import ProductIn
from db import products, database

async def add_product(payload: ProductIn):
    query = products.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_product():
    query = products.select()
    return await database.fetch_all(query=query)


async def get_product(id):
    query = products.select().where(products.c.id == id)
    return await database.fetch_one(query=query)


async def delete_product(id: int):
    query = products.delete().where(products.c.id == id)
    return await database.execute(query=query)


