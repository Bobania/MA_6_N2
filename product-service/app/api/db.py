from datetime import datetime

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, DateTime, Enum, func
from databases import Database
from models import ProductStatuses

# URI подключения к базе данных PostgreSQL
DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'
#DATABASE_URI = 'postgresql://admin:adminadmin@localhost:5432/postgres'

# Создание движка базы данных, который будет использоваться для подключения
engine = create_engine(DATABASE_URI)
# Создание объекта метаданных, который будет содержать информацию о таблицах
metadata = MetaData()

# Определение таблицы 'products' с помощью SQLAlchemy.
products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20)),
    Column('description', String(50)),
    Column('in_stock', Integer),
    Column('price_rub', Integer),
    Column('status', Enum(ProductStatuses))
)
# Создание объекта базы данных
database = Database(DATABASE_URI)



