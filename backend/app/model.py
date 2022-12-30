from pydantic import BaseModel, validator
import datetime

class TicketIn(BaseModel):
    last_name: str
    first_name: str
    patronymic_name: str
    tel: int
    request_text: str

    @validator('last_name')
    def last_name_alpha(cls, v):
        assert v.isalpha(), 'must be alpha'
        return v

    @validator('first_name')
    def first_name_alpha(cls, v):
        assert v.isalpha(), 'must be alpha'
        return v

    @validator('patronymic_name')
    def patronymic_name_alpha(cls, v):
        assert v.isalpha(), 'must be alpha'
        return v

    @validator('tel')
    def tel_int(cls, v):
        assert isinstance(v, int), 'must be integer'
        return v

    @validator('request_text')
    def request_text_(cls, v):
        assert isinstance(v, str), 'must be str'
        return v


class TicketOut(BaseModel):
    application_date: datetime.datetime = datetime.datetime.utcnow().astimezone()
    last_name: str
    first_name: str
    patronymic_name: str
    tel: int
    request_text: str