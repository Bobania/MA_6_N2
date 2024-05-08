import requests

PRODUCT_SERVICE_HOST_URL = 'http://product_service:8000/api/products/get_products'


def is_product_present(product_id: int):
    response = requests.get(PRODUCT_SERVICE_HOST_URL)
    data = response.json()
    id_list = [item['id'] for item in data]
    return product_id in id_list
