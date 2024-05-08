from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import List, Annotated

from models import ProductOut, ProductIn
from db_manager import add_product, get_all_product, get_product, delete_product


products = APIRouter()


@products.post('/create_product', response_model=ProductOut, status_code=201)
async def create_product(payload: Annotated[ProductIn, Depends()]):
    product_id = await add_product(payload)
    response = {
        'id': product_id,
        **payload.dict()
    }
    return response


@products.get('/get_products', response_model=List[ProductOut])
async def get_products():
    return await get_all_product()


@products.get('/{id}/', response_model=ProductOut)
async def get_product_by_id(id: int):
    company = await get_product(id)
    if not company:
        raise HTTPException(status_code=404, detail="Product not found")
    return company


@products.delete('/{id}/', response_model=None)
async def delete_product_by_id(id: int):
    company = await get_product(id)
    if not company:
        raise HTTPException(status_code=404, detail="Product not found")
    return await delete_product(id)

