from models import RefundIn, RefundOut
from db import refunds, database


async def add_refund(payload: RefundIn):
    query = refunds.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_refunds():
    query = refunds.select()
    return await database.fetch_all(query=query)


async def get_refund(id):
    query = refunds.select().where(refunds.c.id == id)
    return await database.fetch_one(query=query)


async def delete_refund(id: int):
    query = refunds.delete().where(refunds.c.id == id)
    return await database.execute(query=query)
