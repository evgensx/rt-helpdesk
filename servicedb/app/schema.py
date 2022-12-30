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
    last_name: str = "Фамилия"
    first_name: str = "Имя"
    patronymic_name: str = "Отчество"
    tel: int = 712345667890
    request_text: str = "Текст обращения"
