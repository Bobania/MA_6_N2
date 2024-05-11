from typing_extensions import List, Annotated
from fastapi import APIRouter, HTTPException, Depends
from models import RefundOut, RefundIn
from db_manager import add_refund, get_refund, get_all_refunds
#from service import is_product_present
import requests
# Создание роутера API
refunds = APIRouter()


# @refunds.post('/create_refund', response_model=RefundIn, status_code=201)
# async def create_refund(payload: Annotated[RefundIn, Depends()]):
#     product_id = payload.product_id
#     if is_product_present(product_id):
#         refund_id = await add_refund(payload)
#         response = {
#             'id': refund_id,
#             **payload.dict()
#         }
#         return response
#     else:
#         raise HTTPException(status_code=404, detail=f"Product with given id:{product_id} not found")


@refunds.get('/get_refunds', response_model=List[RefundOut])
async def get_refunds():
    try:
        result = await get_all_refunds()
        if result is None:
            raise HTTPException(status_code=404, detail='refunds not found')
        return result
    except HTTPException as http_exc:
        # Переадресация исключений от функции get_all_payments()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')

@refunds.get('/{id}/', response_model=RefundOut)
async def get_refund_by_id(id: int):
    try:
        refunds_by_id = await get_refund(id)
        if not refunds_by_id:
            raise HTTPException(status_code=404, detail="refund not found")
        return refunds_by_id
    except HTTPException as http_exc:
        # Переопределение исключений от функции get_payment()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


# @refunds.delete('/delete_refunds/{id}/', response_model=None)
# async def delete_refund_from_db(id: int):
#     try:
#         refunds_by_id = await get_refund(id)
#         if not refunds_by_id:
#             raise HTTPException(status_code=404, detail='Payment not found')
#         await delete_refund(id)
#         return {'message': f'Payment with ID {id} has been successfully deleted'}
#     except HTTPException as http_exc:
#         # Переопределение исключений от функции get_payment()
#         raise http_exc
#     except Exception as e:
#         raise HTTPException(status_code=500, detail='Internal server error')