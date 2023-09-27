import sqlite3
from sqlalchemy import create_engine,Column,Integer,String,MetaData,Table,ForeignKey

DATABASE_URI = 'sqlite:///sipus.db'
engine = create_engine(DATABASE_URI,echo=True)
metadata = MetaData()


#Definisi tabel
book = Table('Book',metadata,
    Column('id',Integer,primary_key=True),
    Column('title',String),
    Column('author',String),
    Column('genre',String),
    Column('stock',Integer)
)

borrowing = Table('Borrowing',metadata,
    Column('id',Integer,primary_key=True),
    Column('id_book',Integer,ForeignKey('book.id')), #Foreign key to ID of table Book
    Column('user_id',String),
    Column('borrow_date',String),
    Column('return_date',String)
)


#Membuat tabel
metadata.create_all(engine)

print("sipus.db created!!")

