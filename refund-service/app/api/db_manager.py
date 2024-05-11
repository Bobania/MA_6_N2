from models import RefundIn, RefundOut
from db import refunds, database
from fastapi import HTTPException


# Функция для добавления нового возврата в базу данных.
async def add_refund(payload: RefundIn):
    try:
        query = refunds.insert().values(**payload.dict())
        return await database.execute(query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')

# Функция для получения списка всех возвратов из базы данных.
async def get_all_refunds():
    try:
        query = refunds.select()
        result = await database.fetch_all(query=query)
        if result:
            return result
        raise HTTPException(status_code=404, detail='refunds not found')
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')

# Функция для получения возврата по его ID.
async def get_refund(id):
    try:
        query = refunds.select().where(refunds.c.id == id)
        result = await database.fetch_one(query=query)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


# async def get_product_id(product_id: int):
#     try:
#         query = refunds.select().where(refunds.c.product_id == product_id)
#         return await database.fetch_one(query=query)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail='Internal server error')
#
#
# async def delete_refund(id: int):
#     try:
#         query = refunds.delete().where(refunds.c.id == id)
#         result = await database.execute(query=query)
#         return result
#     except HTTPException as http_exc:
#         raise http_exc
#     except Exception as e:
#         raise HTTPException(status_code=500, detail='Internal server error')
