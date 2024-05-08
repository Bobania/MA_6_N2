from typing_extensions import List, Annotated
from fastapi import APIRouter, HTTPException, Depends
from models import RefundOut, RefundIn
from db_manager import add_refund, get_refund, get_all_refunds, delete_refund
from service import is_product_present
import requests

refunds = APIRouter()


@refunds.post('/create_refund', response_model=RefundIn, status_code=201)
async def create_refund(payload: Annotated[RefundIn, Depends()]):
    product_id = payload.product_id
    if is_product_present(product_id):
        refund_id = await add_refund(payload)
        response = {
            'id': refund_id,
            **payload.dict()
        }
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Product with given id:{product_id} not found")


@refunds.get('/get_refunds', response_model=List[RefundOut])
async def get_refunds():
    return await get_all_refunds()


@refunds.get('/{id}/', response_model=RefundOut)
async def get_refund_by_id(id: int):
    refunds_by_id = await get_refund(id)
    if not refunds_by_id:
        raise HTTPException(status_code=404, detail="Refund not found")
    return refunds_by_id


@refunds.delete('/delete_refunds/{id}/', response_model=None)
async def delete_refund_from_db(id: int):
    refunds_by_id = await get_refund(id)
    if not refunds_by_id:
        raise HTTPException(status_code=404, detail="Refund not found")
    await delete_refund(id)
    return {"message": f"Refund with ID {id} has been successfully deleted."}