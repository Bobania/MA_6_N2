from fastapi import HTTPException

from models import ProductIn
from db import products, database


# Функция для добавления нового продукта в базу данных.
async def add_product(payload: ProductIn):
    query = products.insert().values(**payload.model_dump())
    return await database.execute(query=query)


# Функция для получения списка всех продуктов из базы данных.
async def get_all_product():
    try:
        query = products.select()
        result = await database.fetch_all(query=query)
        if result:
            return result
        raise HTTPException(status_code=404, detail='products not found')
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


# Функция для получения продукта по его ID.
async def get_product(id):
    try:
        query = products.select().where(products.c.id == id)
        result = await database.fetch_one(query=query)
        if result is None:
            raise HTTPException(status_code=404, detail='product not found')
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')



# Функция для удаления продукта по его ID.
async def delete_product(id: int):
    try:
        query = products.delete().where(products.c.id == id)
        result = await database.execute(query=query)
        if result == 0:
            raise HTTPException(status_code=404, detail='product not found')
        return result
    except HTTPException as http_exc:
        raise http_exc





# async def get_all_product():
#     query = products.select()
#     return await database.fetch_all(query=query)
#
#
# async def get_product(id):
#     query = products.select().where(products.c.id == id)
#     return await database.fetch_one(query=query)
#
#
# async def delete_product(id: int):
#     query = products.delete().where(products.c.id == id)
#     return await database.execute(query=query)
