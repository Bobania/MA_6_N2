from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, create_engine, ARRAY, Enum, func)
from databases import Database
from models import RefundMethod

DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'
#DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'


# Создание движка базы данных, который будет использоваться для подключения
engine = create_engine(DATABASE_URI)
# Создание объекта метаданных, который будет содержать информацию о таблицах
metadata = MetaData()
# Определение таблицы 'refund' с помощью SQLAlchemy.
refunds = Table(
    'refund',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('product_id', Integer),
    Column('status', Enum(RefundMethod))
)
# Создание объекта базы данных
database = Database(DATABASE_URI)

