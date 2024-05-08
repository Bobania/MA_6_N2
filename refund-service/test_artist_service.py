import requests

class ArtistsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_companies(self):
        url = self.base_url
        res = requests.get(url).json()
        return res

    def get_company_by_id(self, company_id: int):
        url = f"{self.base_url}{company_id}"
        res = requests.get(url).json()
        return res

def test_get_all_companies(api: ArtistsAPI):
    res = api.get_all_companies()
    assert(res == [{'artists_id': 1,
     'name': 'Kany West',
     'age': '47',
     'auditions': '1 billion',
     'genre': 'rap, R&B, electronic, gospel'},
    {'artists_id': 2,
     'name': 'Валерий Меладзе',
     'age': '58',
     'auditions': '45 millions',
     'genre': 'поп, рок, эстрадная песня'},
    {'artists_id': 3,
     'name': 'Billie Eilish',
     'age': '22',
     'auditions': '300 millions',
     'genre': 'rap, pop'},
    {'artists_id': 4,
     'name': 'The Weeknd',
     'age': '34',
     'auditions': '700 millions',
     'genre': 'rap, R&B'},
    {'artists_id': 5,
     'name': 'Eminem',
     'age': '51',
     'auditions': '1 billion',
     'genre': 'rap, hip-hop'}])

def test_get_company_by_id(api: ArtistsAPI):
    res = api.get_company_by_id(1)
    assert(res == {'artists_id': 1,
     'name': 'Kany West',
     'age': '47',
     'auditions': '1 billion',
     'genre': 'rap, R&B, electronic, gospel'})

def test_get_company_by_id_invalid(api: ArtistsAPI):
    # Проверка на получение информации о несуществующей компании
    res = api.get_company_by_id(1000)
    assert(res == {})  # Предполагаем, что при запросе несуществующей компании API возвращает пустой словарь

def test_get_company_by_name(api: ArtistsAPI):
    # Проверка получения информации о компании по имени
    companies = api.get_all_companies()
    company_name = companies[0]['name']  # Предполагаем, что компания существует в списке
    res = api.get_company_by_name(company_name)
    assert(res['name'] == company_name)

if __name__ == '__main__':
    URL = 'http://127.0.0.1:80/api/v1/artists/'
    api = ArtistsAPI(URL)
    test_get_company_by_id(api)
    test_get_all_companies(api)
    test_get_company_by_id_invalid(api)
    test_get_company_by_name(api)