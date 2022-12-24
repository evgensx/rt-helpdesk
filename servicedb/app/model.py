
from app.db import db, metadata
from sqlalchemy import Table, Column, Integer, Identity, DateTime, String, BigInteger, Text

# Define table
tickets = Table("tickets", metadata,
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
        _query = tickets.select()
        _tickets = await db.fetch_all(_query)
        return _tickets

    @classmethod
    async def create(cls, **ticket):
        print("!TICKET:", ticket)
        _query = tickets.insert().values(ticket)
        print("!QUERY:", _query)
        _last_record_id = await db.execute(_query)
        print("!ID:", _last_record_id)
        return _last_record_id
