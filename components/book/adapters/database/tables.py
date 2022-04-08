from sqlalchemy import (
    MetaData, Table, Column, Integer, String
)

# naming_convention = {
#     'ix': 'ix_%(column_0_label)s',
#     'uq': 'uq_%(table_name)s_%(column_0_name)s',
#     'ck': 'ck_%(table_name)s_%(constraint_name)s',
#     'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
#     'pk': 'pk_%(table_name)s'
# }
#
# metadata = MetaData(naming_convention=naming_convention)

metadata = MetaData()

books = Table(
    'books',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('year', Integer, nullable=False),
)
