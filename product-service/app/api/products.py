from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import List, Annotated

from models import ProductOut, ProductIn
from db_manager import add_product, get_all_product, get_product, delete_product


products = APIRouter()


@products.post('/create_product', response_model=ProductOut, status_code=201)
async def create_product(payload: Annotated[ProductIn, Depends()]):
    try:
        product_id = await add_product(payload)
        response = {
            'id': product_id,
            **payload.model_dump()
        }
        return response
    except HTTPException as http_exc:
        # Переадресация исключений от функции add_purchase
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


@products.get('/get_products', response_model=List[ProductOut])
async def get_products():
    try:
        return await get_all_product()
    except HTTPException as http_exc:
        # Переадресация исключений от функции get_all_purchase()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


@products.get('/{id}/', response_model=ProductOut)
async def get_product_by_id(id: int):
    try:
        product_by_id = await get_product(id)
        return product_by_id
    except HTTPException as http_exc:
        # Переопределение исключений от функции get_purchase()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


@products.delete('/{id}/', response_model=None)
async def delete_product_by_id(id: int):
    try:
        product_by_id = await get_product(id)
        if not product_by_id:
            raise HTTPException(status_code=404, detail='product not found')
        await delete_product(id)
        return {'message': f'product with ID {id} has been successfully deleted'}
    except HTTPException as http_exc:
        # Переопределение исключений от функции delete_purchase()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')

