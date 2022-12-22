import asyncio
import aiormq
from fastapi import FastAPI, WebSocket, responses
from pydantic import BaseModel
import datetime
import logging
import psycopg2
import json

logging.basicConfig(level=logging.INFO)


class AioRabbitClient:
    """Async io client for rabbitmq. Consumer for queue helpdessk_queue.\n
    Connect to server, read message and return json object to datebase client.\n
    Depends: module 'aiormq'
    """

    def __init__(self, vhost: str | None = '', host: str = 'localhost', port: int | str = 5672, user: str = 'guest',
                 password: str = 'guest', queue: str = 'queue1', exchange: str = 'amq.direct',
                 routing_key: str = "helpdesk_routing_key") -> None:
        self.url = f"amqp://{user}:{password}@{host}:{port}/{vhost}"
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key

    async def on_message(self, message: aiormq.abc.DeliveredMessage) -> str:
        """On_message doesn't necessarily have to be defined as async. Here it is to show that it's possible."""
        logging.info(f"[+] Received message {message!r}")
        logging.info(f"Message key:body is: {message.delivery.routing_key!r}:{message.body!r}")
        await message.channel.basic_ack(message.delivery.delivery_tag)
        return message.body

    async def consume(self) -> None:
        # Perform connection
        connection = await aiormq.connect(url=self.url)

        # Creating a channel
        channel = await connection.channel()
        await channel.basic_qos(prefetch_count=1)

        # Declaring exchange
        await channel.exchange_declare(exchange=self.exchange, durable=True)

        # Declaring queue
        declare_ok = await channel.queue_declare(queue=self.queue, durable=True)

        # Binding the queue to the exchange
        await channel.queue_bind(declare_ok.queue, exchange=self.exchange, routing_key=self.routing_key)

        # Start listening the queue with name 'task_queue'
        await channel.basic_consume(queue=declare_ok.queue, consumer_callback=self.on_message)


class PgClient():
    """Depends: (module) psycopg2.  Client for writing into db helpdesk, 'requests' table"""

    def __init__(self, user="admin", password="admin", database="helpdesk", host="172.16.0.6", port="5432",
                 table="requests") -> None:
        self.table_name: str = table
        self.is_connect = None
        self._table_keys: str | None = None
        self.dsn = f"user={user} password={password} dbname={database} host={host} port={port}"
        self._insert_column: str

    def connect(self):
        """Connect to your postgres DB"""
        try:
            conn = psycopg2.connect(self.dsn)
            self.is_connect = conn.status
            logging.info(
                f"[+] Database connection established. Status: {self.is_connect}")
            return conn
        except:
            return logging.info("[-] I am unable to connect to the database")

    def table_model(self, *args):
        schema = ""
        keys = []
        for i in args:
            keys.append(i[0])
            schema += " ".join(i)
            schema += ", "
        schema = schema.rstrip(", ")
        self._table_keys = keys
        self._insert_column = ", ".join(self._table_keys[1:])
        # logging.info(self._table_keys)
        # logging.info(schema)
        logging.info("[+] Table model '%s' was executed", self.table_name)
        _query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({schema});"
        # logging.debug("Query: %s", _query)
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(_query)
        conn.close()

    def select(self, size=0):
        """Execute a query"""
        cur = self.connect().cursor()
        col = self._table_keys[0]
        if size > 1:
            query = f"WITH temp AS (SELECT * FROM {self.table_name} ORDER BY {col} DESC LIMIT {size}) \
                SELECT * FROM temp ORDER BY {col};"
        elif size == 1:
            query = f"SELECT * FROM {self.table_name} ORDER BY {col} DESC LIMIT 1;"
        elif size == 0:
            query = f"SELECT * FROM {self.table_name};"
        else:
            return 0
        cur.execute(query)
        return cur

    def get_list(self, values: list | tuple):
        keys = self._table_keys
        result = []
        if type(values) == list:
            for value in values:
                result.append(dict(zip(keys, value)))
            return result
        else:
            return logging.info(f"Error type is {type(values)}")

    def get_all(self, query):
        """query = self.select(size: int | None)"""
        list_tuples = query.fetchall()
        result = self.get_list(list_tuples)
        # logging.info()
        return result

    def insert(self):
        _conn = self.connect()
        _cur = _conn.cursor()
        _table = self.table_name
        _column_names = se
        _values = []
        _query = f"INSERT INTO {_table} ({_column_names}) \
            VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');"
        _cur.execute(_query)

# -------------------------------------------------------------------------------------------------


class ResponsesOut(BaseModel):
    id: int
    date_application: datetime.datetime
    last_name: str
    first_name: str
    patronymic_name: str
    tel: int
    request_text: str


class RequestsIn(BaseModel):
    date_application: datetime.datetime = datetime.datetime.utcnow().astimezone()
    last_name: str = "Ivanov"
    first_name: str = "Ivan"
    patronymic_name: str = "Ivanovich"
    tel: int = 71234567890
    request_text: str = "Help me pls"


class MessagesIn(BaseModel):
    count: int = 1
    ackmode: str = "ack_requeue_false"
    encoding: str = "auto"
    truncate: int = 50000
    tags: str


class MessagesOut(BaseModel):
    payload: str


# -------------------------------------------------------------------------------------------------
db = PgClient()
# db.connect()

db.table_model(
    ("id", "integer", "CONSTRAINT", "firstkey", "PRIMARY KEY"),
    ("date_application", "date"),
    ("last_name", "text"),
    ("first_name", "text"),
    ("patronymic_name", "text"),
    ("tel", "text"),
    ("request_text", "text"))

app = FastAPI()

client = AioRabbitClient("helpdesk", "172.16.0.4",
                         user="admin", password="admin", queue="helpdesk_queue")


@app.on_event('startup')
async def sturtup():
    loop = asyncio.get_running_loop()
    task1 = loop.create_task(client.consume(), name="Consumer RabbitMQ Client")
    await task1

@app.get("/get/", response_model=list[ResponsesOut])
async def read_requests():
    query = db.select()
    return db.get_all(query)

# @app.post("/get_messages/", response_model=MessagesOut)
# async def get_messages(messages: MessagesIn):
#     return messages


@app.get("/get/{size}", response_model=list[ResponsesOut])
async def read_requests(size: int) -> list[RequestsIn]:
    query = db.select(size)
    return db.get_all(query)

# @app.post("/items/")
# async def create_items(item: Item):
#     return item
