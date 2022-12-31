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

    @classmethod
    async def get_same_items(cls, size: int):
        if isinstance(size, int):
            if size == 1:
                _query = tickets_table.select().order_by(tickets_table.c.id.desc()).limit(1)
            elif size > 1:
                subq = tickets_table.select().order_by(tickets_table.c.id.desc()).limit(size).cte()
                _query = (subq.select().order_by(subq.c.id))
            else:
                _query = tickets_table.select().order_by(tickets_table.c.id).limit(1)
        _same_tickets = await db.fetch_all(_query)
        return _same_tickets
