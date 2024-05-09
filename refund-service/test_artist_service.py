#E2E

import requests
import random
import requests_mock
import enum
from datetime import datetime, timedelta


class RefundMethod(enum.Enum):
    PAY = 'refund_pay'
    NOT_PAY = 'not_refund_pay'



base_url = 'http://0.0.0.0:8080/api/refunds/'

product_id: int
status: RefundMethod

mock_refund_data = [
    {'id': 1, 'product_id': 3,   'status': 'refund_pay' },
    {'id': 2, 'product_id': 4,   'status': 'refund_pay'},
    {'id': 3, 'product_id': 5,   'status': 'not_refund_pay'}
]

def mock_request(adapter):
    adapter.register_uri('GET', f'{base_url}get_refunds', json={'detail': 'Not Found'}, status_code=404)
def test_get_refund_empty() -> None:
    with requests_mock.Mocker() as m:
        mock_request(m)
        response = requests.get(f'{base_url}get_refunds')
        assert response.json() == {'detail': 'Not Found'}
        assert response.status_code == 404


def mock_request_with_data_by_id(adapter, refund_id, refund_data):
    # Регистрация маршрута для конкретного ID платежа
    adapter.register_uri('GET', f'{base_url}{refund_id}/', json=refund_data, status_code=200)


# Тест получения payments по id
def test_get_payment_by_id_found():
    with requests_mock.Mocker() as m:
        # Регистрации маршрута с помощью адаптера
        mock_request_with_data_by_id(m, mock_refund_data[0]['id'], mock_refund_data[0])
        response = requests.get(f'{base_url}{mock_refund_data[0]["id"]}/')
        assert response.status_code == 200
        assert response.json() == mock_refund_data[0]


def mock_request_with_data_by_id(adapter, refund_id, refund_data):
    # Регистрация маршрута для конкретного ID платежа
    adapter.register_uri('GET', f'{base_url}{refund_id}/', json=refund_data, status_code=200)


# Тест получения refunds по id
def test_get_refund_by_id_found():
    with requests_mock.Mocker() as m:
        # Регистрации маршрута с помощью адаптера
        mock_request_with_data_by_id(m, mock_refund_data[0]['id'], mock_refund_data[0])
        response = requests.get(f'{base_url}{mock_refund_data[0]["id"]}/')
        assert response.status_code == 200
        assert response.json() == mock_refund_data[0]


# Тест получения несуществующего refund
def test_get_refund_by_id_not_found():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', f'{base_url}123/', json={'detail': 'refunds not found'}, status_code=404)
        response = requests.get(f'{base_url}123/')
        assert response.status_code == 404
        assert response.json() == {'detail': 'refunds not found'}


# Тест удаления refund по id {base_url}{id}
def test_delete_refund():
    with requests_mock.Mocker() as m:
        # Регистрации маршрута с помощью адаптера
        mock_request_with_data_by_id(m, 1, mock_refund_data)
        # Регистрация маршрута для DELETE запроса
        m.delete(f'{base_url}1/', json={'message': 'refund with ID 1 has been successfully deleted'}, status_code=200)
        m.delete(f'{base_url}99/', json={'detail': 'refund not found'}, status_code=404)
        response = requests.delete(f'{base_url}1/')
        # Проверка успешного удаления payments
        assert response.status_code == 200
        assert response.json() == {'message': 'refund with ID 1 has been successfully deleted'}
        # Проверка попытки удаления несуществующего payments
        response = requests.delete(f'{base_url}99/')
        assert response.status_code == 404
        assert response.json() == {'detail': 'refund not found'}

