from pydantic import BaseModel
import datetime


class TicketsOut(BaseModel):
    id: int
    application_date: datetime.datetime
    last_name: str
    first_name: str
    patronymic_name: str
    tel: int
    request_text: str


class TicketIn(BaseModel):
    application_date: datetime.datetime = datetime.datetime.utcnow().astimezone()
    last_name: str = "Ivanov"
    first_name: str = "Ivan"
    patronymic_name: str = "Ivanovich"
    tel: int = 71234567890
    request_text: str = "Help me pls"

    # class Config:
    #     orm_mode = True
