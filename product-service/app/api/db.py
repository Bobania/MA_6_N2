from datetime import datetime

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, DateTime, Enum, func
from databases import Database
from models import ProductStatuses

#DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'
DATABASE_URI = 'postgresql://admin:adminadmin@localhost:5432/postgres'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20)),
    Column('description', String(20)),
    Column('in_stock', Integer),
    Column('price_rub', Integer),
    Column('status', Enum(ProductStatuses))
)

database = Database(DATABASE_URI)




