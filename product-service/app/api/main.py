from fastapi import FastAPI, HTTPException, Form, Header
from .products import products
from db import metadata, database, engine
#from keycloak import KeycloakOpenID
from prometheus_fastapi_instrumentator import Instrumentator
from keycloak.keycloak_openid import KeycloakOpenID


# Создание таблиц в базе данных на основе метаданных
metadata.create_all(engine)

#app = FastAPI(title="Интернет-магазин настольных игр")
app = FastAPI(title='Интернет магазин настольных игр', openapi_url="/api/products/openapi.json",
              docs_url="/docs")
Instrumentator().instrument(app).expose(app)
# Настройка для сбора метрик Prometheus и их предоставления.
#productuser
#admin

# Конфигурация клиента Keycloak
#KEYCLOAK_URL = "http://localhost:8010/"
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "productClient"
KEYCLOAK_REALM = "master"
KEYCLOAK_CLIENT_SECRET = "O5rj3VqtV6wDcG8rKxVKlegMiFLEiyuv"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


# Эндпоинт для логина, который возвращает токен при успешной аутентификации.
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=['password'],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='Failed to get token')


# Функция для проверки роли пользователя в токене.
def user_got_role(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if 'productRole' not in token_info['realm_access']['roles']:
            raise HTTPException(status_code=403, detail='Access denied')
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token or access denied')


# Эндпоинт для подключения к базе данных, если пользователь имеет правильную роль.
@app.put("/connect")
async def startup(token: str = Header()):
    if user_got_role(token):
        await database.connect()
        return {'message': 'Database connected'}
    else:
        return "Wrong JWT Token"


# Обработчик события для отключения от базы данных при завершении работы приложения.
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()



# @app.on_event('startup')
# async def startup():
#     await database.connect()
#     return 'Database connected'
#
# @app.on_event("startup")
# async def startup_event():
#     await startup()

# Регистрация роутера, который обрабатывает запросы к API склада.

app.include_router(products, prefix='/api/products', tags=['Склад'])
