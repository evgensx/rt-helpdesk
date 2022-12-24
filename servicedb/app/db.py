from os import environ as env
from databases import Database
import asyncpg.exceptions
import sqlalchemy
from sqlalchemy import MetaData, dialects
# from model import tickets
# from sqlalchemy.ext.asyncio import create_async_engine


DATABASE_URL = env.get("DATABASE_URL")
db = Database(DATABASE_URL)
metadata = MetaData()
dialect = dialects.postgresql.dialect()

# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )
# metadata.create_all(engine)


class Engine:
    @classmethod
    async def create_all(cls):
        try:
            # query = tickets.select('id')
            # await db.execute(query)
            query = await db.execute('SELECT id FROM tickets LIMIT 1')
        except asyncpg.exceptions.UndefinedTableError:
            # Create tables
            for table in metadata.tables.values():
                # Set `if_not_exists=False` if you want the query to throw an
                # exception when the table already exists
                schema = sqlalchemy.schema.CreateTable(
                    table, if_not_exists=True)
                query = str(schema.compile(dialect=dialect))
                await db.execute(query)
