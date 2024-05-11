import requests
from fastapi import HTTPException
from requests import RequestException

REFUND_SERVICE_URL = 'http://refund_service:8020/api/refund/get_all_refunds'

# Асинхронная функция для получения всех возвратов от сервиса возвратов.
async def get_all_refunds():
    try:
        response = requests.get(REFUND_SERVICE_URL)
        response.raise_for_status()
        data = response.json()
        return data
    except RequestException as e:
        raise HTTPException(status_code=500, detail = 'Service none')