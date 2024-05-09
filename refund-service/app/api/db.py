from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, create_engine, ARRAY, Enum, func)
from databases import Database
from models import RefundMethod

DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'
#DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

refunds = Table(
    'refund',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('product_id', Integer),
    Column('status', Enum(RefundMethod))
)

database = Database(DATABASE_URI)

