from os import getenv
from databases import Database
import asyncpg.exceptions
import sqlalchemy
from sqlalchemy import dialects, schema
import logging
# from sqlalchemy.ext.asyncio import create_async_engine


DATABASE_URL = getenv(
    'DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
db = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
dialect = dialects.postgresql.dialect()


class Engine:
    @classmethod
    async def create_all(cls):
        try:
            from app.model import tickets_table
            # Checking if a table exists
            logging.info('Checking table')
            # await db.execute(select(tickets_table.c.id))
            await db.execute('SELECT id FROM tickets LIMIT 1')
        except asyncpg.exceptions.UndefinedTableError:
            # Create tables
            logging.info('Creating all tables')
            for table in db.tables.values():
                # Set `if_not_exists=False` if you want the query to throw an
                # exception when the table already exists
                _schema = schema.CreateTable(table, if_not_exists=True)
                query = str(_schema.compile(dialect=dialect))
                await db.execute(query)


class DbCli:
    @classmethod
    async def connect(cls):
        await db.connect()
        await Engine.create_all()
        logging.info('[+] Connected to postgresql\n')

    @classmethod
    async def disconnect(cls):
        await db.disconnect()
        logging.info('[+] Disconnected from postgresql\n')


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )
# metadata.create_all(engine)
