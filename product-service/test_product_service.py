#Unit
import tracemalloc
tracemalloc.start()
import random
import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.api.models import ProductIn, ProductStatuses
from app.api.db_manager import get_all_product, get_product, add_product, delete_product
from app.api.products import (get_product_by_id, get_products, create_product,  delete_product_by_id)


name = "TestGame"
description = "Test Description"
in_stock = random.randint(1, 100)
price_rub = random.randint(1, 100)
status = random.choice(list(ProductStatuses))


mock_product_data = [
  {
    'name': name,
    'description': description,
    'in_stock': in_stock,
    'price_rub': price_rub,
    'status': status
  },
  {
    'name': name,
    'description': description,
    'in_stock': in_stock,
    'price_rub': price_rub,
    'status': status
  },
  {
    "name": name,
    "description": description,
    "in_stock": in_stock,
    "price_rub": price_rub,
    "status": status
  }
]


# models.py Тесты

# Проверка полей таблицы
@pytest.fixture()
def any_product() -> ProductIn:
    return ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub, status=status)


def test_product_creation(any_product: ProductIn):
  assert dict(any_product) == {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status}


# Тесты для проверки валидации полей таблицы продуктов
def test_product_name(any_product: ProductIn):
    with pytest.raises(Exception):
        ProductIn(description=description, in_stock=in_stock, price_rub=price_rub, status=status)
    with pytest.raises(Exception):
        ProductIn(name=123, description=description, in_stock=in_stock, price_rub=price_rub, status=status)

def test_product_description(any_product: ProductIn):
    with pytest.raises(Exception):
        ProductIn(name=name, description=42, in_stock=in_stock, price_rub=price_rub, status=status)

def test_product_in_stock(any_product: ProductIn):
    with pytest.raises(Exception):
        ProductIn(name=name, description=description, in_stock='-', price_rub=price_rub, status=status)
    with pytest.raises(Exception):
        ProductIn(name=name, description=description, price_rub=price_rub, status=status)

def test_product_price_rub(any_product: ProductIn):
    with pytest.raises(Exception):
        ProductIn(name=name, description=description, in_stock=in_stock, price_rub='-', status=status)


def test_product_status(any_product: ProductIn):
    with pytest.raises(Exception):
        ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub)
    with pytest.raises(Exception):
        ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub, status='-')
    with pytest.raises(Exception):
        ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub, status=1)






# db_manager.py Тесты

# Тест добавления продуктов
@pytest.mark.asyncio
async def test_add_product():
    test_data = ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub, status=status)
    expected_response = {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status}
    with patch('app.api.db_manager.database.execute', new_callable=AsyncMock) as mock_database:
        mock_database.return_value = expected_response
        response = await add_product(test_data)
        assert response == expected_response


# Тест получения всех продуктов
@pytest.mark.asyncio
async def test_get_all_product():
    expected_response = [
        {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status},
        {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status},
        {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status}
    ]
    with patch('app.api.db_manager.database', new_callable=AsyncMock) as mock_database:
        mock_database.fetch_all.return_value = expected_response
        response = await get_all_product()
        assert response == expected_response
        mock_database.fetch_all.return_value = []
        with pytest.raises(HTTPException) as exc_info:
            await get_all_product()
        assert exc_info.value.status_code == 404


# Тест получения продукта по id
@pytest.mark.asyncio
async def test_get_product():
    test_data = 1
    expected_response = {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status}
    with patch('app.api.db_manager.database.fetch_one', new_callable=AsyncMock) as mock_database:
        mock_database.return_value = expected_response
        response = await get_product(test_data)
        assert response == expected_response
    # Тестирование исключения, если purchase не найден
    with patch('app.api.db_manager.database.fetch_one', new_callable=AsyncMock) as mock_database:
        mock_database.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await get_product(test_data)
        assert exc_info.value.status_code == 404

# Тест удаления продукта по id
@pytest.mark.asyncio
async def test_delete_product():
    test_data = 1
    expected_response = [
        {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status},
        {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status},
        {'name': name, 'description': description, 'in_stock': in_stock, 'price_rub': price_rub, 'status': status}
    ]
    with patch('app.api.db_manager.database', new_callable=AsyncMock) as mock_database:
        mock_database.fetch_all.return_value = expected_response
        mock_database.execute.return_value = test_data
        response = await delete_product(test_data)
        assert response == test_data

    async def mock_execute(query):
        assert 'WHERE products.id =' in str(query)
        return 0

    # Тест удаления несуществующего продукта
    with patch('app.api.db_manager.database.execute', new=mock_execute):
        with pytest.raises(HTTPException) as exc_info:
            await delete_product(4)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'product not found'

#-------------------------------------------------------------------------------------------------------------------

# #Тесты 1/4
# #Тест добавления продукта
# # @pytest.mark.asyncio
# # async def test_add_product():
# #     test_data = ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub, status=status)
# #     with patch('app.api.db_manager.database.execute', new_callable=AsyncMock) as mock_execute:
# #         mock_execute.return_value = test_data
# #         response = await add_product(test_data)
# #         assert response == test_data



# @pytest.mark.asyncio
# async def test_get_all_product():
#     with patch('app.api.db_manager.database', new_callable=AsyncMock) as mock_database:
#         mock_database.fetch_all.return_value = mock_product_data
#         response = await get_all_product()
#         assert response == mock_product_data
#         mock_database.fetch_all.return_value = []
#         with pytest.raises(HTTPException) as exc_info:
#             await get_all_product()
#         assert exc_info.value.status_code == 404
#
#
# # Тест получения product по id
# @pytest.mark.asyncio
# async def test_get_product():
#     with patch('app.api.db_manager.database.fetch_one', new_callable=AsyncMock) as mock_db:
#         mock_db.return_value = mock_product_data[1]
#         response = await get_product(1)
#         assert response == mock_product_data[1]
#     # Тестирование исключения, если product не найден
#     with patch('app.api.db_manager.database.fetch_one', new_callable=AsyncMock) as mock_db:
#         mock_db.return_value = None
#         with pytest.raises(HTTPException) as exc_info:
#             await get_product(1)
#         assert exc_info.value.status_code == 404
#
# # Тест получения product по id
# @pytest.mark.asyncio
# async def test_get_product():
#     with patch('app.api.db_manager.database.fetch_one', new_callable=AsyncMock) as mock_db:
#         mock_db.return_value = mock_product_data[1]
#         response = await get_product(1)
#         assert response == mock_product_data[1]
#     # Тестирование исключения, если producte не найден
#     with patch('app.api.db_manager.database.fetch_one', new_callable=AsyncMock) as mock_db:
#         mock_db.return_value = None
#         with pytest.raises(HTTPException) as exc_info:
#             await get_product(1)
#         assert exc_info.value.status_code == 404
#
#
# # Тест удаления product по id
#
# @pytest.mark.asyncio
# async def test_delete_product():
#     with patch('app.api.db_manager.database', new_callable=AsyncMock) as mock_delete_product:
#         mock_delete_product.fetch_all.return_value = mock_product_data
#         mock_delete_product.execute.return_value = 1
#         response = await delete_product(1)
#         assert response == 1
#
#     async def mock_execute(query):
#         # Обновите утверждение, чтобы оно соответствовало фактическому запросу
#         assert 'WHERE products.id =' in str(query)
#         return 0
#
#     # Тест удаления несуществующего продукта
#     with patch('app.api.db_manager.database.execute', new=mock_execute):
#         with pytest.raises(HTTPException) as exc_info:
#             await delete_product(10)
#         assert exc_info.value.status_code == 404
#         assert exc_info.value.detail == 'product not found'
#
#
# # products.py Тесты
#
#
# # Тест добавления product
# @pytest.mark.asyncio
# async def test_create_product():
#     test_data = ProductIn(name=name, description=description, in_stock=in_stock, price_rub=price_rub, status=status)
#     test_response_data = {'id': 1, **test_data.model_dump()}
#     with patch('app.api.products.add_product', new_callable=AsyncMock) as mock_create_product:
#         mock_create_product.return_value = 1
#         response = await create_product(test_data)
#         mock_create_product.assert_awaited_with(test_data)
#         assert response == test_response_data
#     with patch('app.api.products.get_all_product', new_callable=AsyncMock) as mock_create_product:
#         mock_create_product.side_effect = Exception()
#         with pytest.raises(HTTPException) as exc_info:
#             await create_product(test_data)
#         assert exc_info.value.status_code == 500
#         assert exc_info.value.detail == 'Internal server error'
#
#
# # Тест получения всех product
# @pytest.mark.asyncio
# async def test_get_products():
#     with patch('app.api.products.get_all_product', new_callable=AsyncMock) as mock_get_all:
#         mock_get_all.return_value = mock_product_data
#         response = await get_products()
#         assert response == mock_product_data
#     # идентификатор продукта в get_product
#     product_id = 1
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product:
#         mock_get_product.side_effect = Exception()
#         with pytest.raises(HTTPException) as exc_info:
#             await get_product(product_id)
#         assert exc_info.value.status_code == 500
#         assert exc_info.value.detail == 'Internal server error'
#
#
#
# # Тест получения всех product по id
# @pytest.mark.asyncio
# async def test_get_product_by_id():
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product:
#         mock_get_product.return_value = mock_product_data
#         response = await get_product_by_id(1)
#         assert response == mock_product_data
#     # Тестирование исключения, если покупка не найдена
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product:
#         mock_get_product.side_effect = HTTPException(status_code=404, detail='product not found')
#         with pytest.raises(HTTPException) as exc_info:
#             await get_product_by_id(1)
#         assert exc_info.value.status_code == 404
#         assert exc_info.value.detail == 'product not found'
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product:
#         mock_get_product.side_effect = Exception()
#         with pytest.raises(HTTPException) as exc_info:
#             await get_product_by_id(1)
#         assert exc_info.value.status_code == 500
#         assert exc_info.value.detail == 'Internal server error'
#
#
# # Тест удаления всех product по id
# @pytest.mark.asyncio
# async def test_delete_product_by_id():
#     # Первый сценарий: Успешное удаление продукта
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product, \
#          patch('app.api.products.delete_product', new_callable=AsyncMock) as mock_delete_product:
#         mock_get_product.return_value = mock_product_data
#         mock_delete_product.return_value = {'message': f'product with ID {1} has been successfully deleted'}
#         response = await delete_product_by_id(1)
#         assert response == {'message': f'product with ID {1} has been successfully deleted'}
#
#     # Второй сценарий: Продукт не найден, должно быть вызвано исключение HTTPException с кодом 404
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product:
#         mock_get_product.return_value = None
#         with pytest.raises(HTTPException) as exc_info:
#             await delete_product_by_id(2)
#         assert exc_info.value.status_code == 404
#         assert exc_info.value.detail == 'product not found'
#
#     # Третий сценарий: Во время удаления происходит исключение, должно быть вызвано исключение HTTPException с кодом 500
#     with patch('app.api.products.get_product', new_callable=AsyncMock) as mock_get_product, \
#          patch('app.api.products.delete_product', new_callable=AsyncMock) as mock_delete_product:
#         mock_get_product.return_value = mock_product_data
#         mock_delete_product.side_effect = Exception()
#         with pytest.raises(HTTPException) as exc_info:
#             await delete_product_by_id(2)
#         assert exc_info.value.status_code == 500
#         assert exc_info.value.detail == 'Internal server error'