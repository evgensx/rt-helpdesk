import logging
from app.app import app
from app.schema import TicketIn, TicketsOut
from app.model import Ticket as TicketModel


logging.basicConfig(level=logging.DEBUG)

# return all items from database
@app.get("/tickets/", response_model=list[TicketsOut])
async def read_tickets() -> list[TicketsOut]:
    tickets = await TicketModel.get_all()
    logging.info('[x] Get tickets')
    return tickets

# Return last items from database
@app.get("/tickets/{size}", response_model=list[TicketsOut])
async def read_tickets(size: int) -> list[TicketsOut]:
    tickets = await TicketModel.get_same_items(size)
    logging.info('[x] Get some last tickets')
    return tickets

@app.post("/tickets/", response_model=TicketsOut)
async def create_ticket(ticket: TicketIn) -> TicketsOut:
    last_record_id = await TicketModel.create(**ticket.dict())
    return {**ticket.dict(), "id": last_record_id}


