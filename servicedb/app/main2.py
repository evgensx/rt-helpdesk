from pydantic import BaseModel
import databases as _db
import sqlalchemy as sa
import datetime as _dt
import pika
import logging
import json
from fastapi import FastAPI


logging.basicConfig(level=logging.INFO)


# class PikaClient:
#     def __init__(self):
#         self.publish_queue_name: str = 'helpdesk_queue'
#         self.exchange_name = 'amq.direct'
#         self.routing_key_name = 'helpdesk_routing_key'
#         self.credentials = pika.PlainCredentials('admin', 'admin')
#         self.parameters = pika.ConnectionParameters('172.16.0.4', 5672, 'helpdesk', credentials=self.credentials)
#         self.connection = pika.BlockingConnection(self.parameters)
#         self.channel = self.connection.channel()
#         set_exchange = self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct', durable=True,
#                                                      auto_delete=False, internal=False, passive=True)
#         set_queue = self.channel.queue_declare(queue=self.publish_queue_name, durable=True, exclusive=False,
#                                                auto_delete=False)
#         set_bind = self.channel.queue_bind(queue=self.publish_queue_name, exchange=self.exchange_name,
#                                            routing_key=self.routing_key_name)
#         self.callback_queue = set_queue.method.queue
#         self.response = None
#         self.corr_id = None
#         logging.debug('Pika connection initialized')


#     def send_message(self, message: dict):
#         """Method to publish message to RabbitMQ"""
#         try:
#             # Send message method
#             self.channel.basic_publish(self.exchange_name,
#                                        self.publish_queue_name,
#                                        json.dumps(message),
#                                        pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
#             logging.debug('Message publish was confirmed')
#         except pika.excepttions.AuthenticationError:
#             logging.debug('Message could not be confirmed')


#     def on_message_callback(self, channel, method, properties, body):
#         # if self.corr_id = properties.correla
#         logging.info(f'Resived Body: {body} and props: {properties}')


#     def consume(self): # callback
#         self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_message_callback,
#                                    exclusive=False, consumer_tag='servicedb')
#         logging.debug('Established pika async listener')
#         # Start consuming callback
#         self.channel.consume()


# rabbit = PikaClient()
# rabbit.consume()


    # async def process_incoming_message(self, message: dict):
    #     """Processing incoming message from RabbitMQ"""
    #     message.ack()
    #     body = message.body
    #     logging.info('Received message')
    #     if body:
    #         self.process_callable(json.loads(body))


    # def consume(self, loop):
    #     """Setup message listener with the current running loop"""
    #     connection = await connect_robust(host=env('RABBIT_HOST', '127.0.0.1'),
    #                                     port=5672,
    #                                     loop=loop)
    #     channel = await connection.channel()
    #     queue = await channel.declare_queue(env('CONSUME_QUEUE', 'foo_consume_queue'))
    #     await queue.consume(self.process_incoming_message, no_ack=False)
    #     logging.info('Established pika async listener')
    #     return connection




# -------------------------------------------------------------------------------------------------

DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/helpdesk"
db = _db.Database(DATABASE_URL)
metadata = sa.MetaData(schema="public")
pgtable = sa.Table("requests", metadata,
                        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
                        sa.Column("date_application", sa.DateTime(timezone=True)),
                        sa.Column("last_name", sa.String),
                        sa.Column("first_name", sa.String),
                        sa.Column("patronymic_name", sa.String),
                        sa.Column("tel", sa.BigInteger),
                        sa.Column("request_text", sa.Text))
engine = sa.create_engine(DATABASE_URL)
metadata.create_all(engine)


# -------------------------------------------------------------------------------------------------
class Responses(BaseModel):
    id: int
    date_application: _dt.datetime
    last_name: str
    first_name: str
    patronymic_name: str
    tel: int
    request_text: str


class RequestsIn(BaseModel):
    date_application: _dt.datetime = _dt.datetime.utcnow().astimezone()
    last_name: str = "Ivanov"
    first_name: str = "Ivan"
    patronymic_name: str = "Ivanovich"
    tel: int = 71234567890
    request_text: str = "Help me pls"

async def read_requests():
    db.connect()
    query = pgtable.select()
    return await db.fetch_all(query)

print(read_requests())

# -------------------------------------------------------------------------------------------------
# app = FastAPI()

# @app.on_event('startup')
# async def startup() -> None:
#     await db.connect()


# @app.on_event("shutdown")
# async def shutdown() -> None:
#     await db.disconnect()


# @app.get("/get", response_model=list[Responses])
# async def read_requests() -> list[Responses]:
#     query = pgtable.select()
#     return await db.fetch_all(query)


# @app.post("/post", response_model=Responses)
# async def create_request(request: RequestsIn) -> RequestsIn:
#     query = pgtable.insert().values(
#         date_application=request.date_application,
#         last_name=request.last_name,
#         first_name=request.first_name,
#         patronymic_name=request.patronymic_name,
#         tel=request.tel,
#         request_text=request.request_text
#     )
#     last_record_id = await db.execute(query)
#     return {**request.dict(), "id": last_record_id}
