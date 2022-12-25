from app.db import db, metadata
from sqlalchemy import Table, Column, Integer, Identity, DateTime, String, BigInteger, Text

# Define table
tickets_table = Table("tickets", metadata,
                Column("id", Integer, Identity(), primary_key=True),
                Column("application_date", DateTime(timezone=True)),
                Column("last_name", String(length=30)),
                Column("first_name", String(length=20)),
                Column("patronymic_name", String(length=30)),
                Column("tel", BigInteger),
                Column("request_text", Text))


class Ticket:
    """Ticket responses models class"""
    @classmethod
    async def get_all(cls):
        _query = tickets_table.select()
        _tickets = await db.fetch_all(_query)
        return _tickets

    @classmethod
    async def create(cls, **ticket):
        print(ticket)
        _query = tickets_table.insert().values(ticket)
        _last_record_id = await db.execute(_query)
        return _last_record_id
