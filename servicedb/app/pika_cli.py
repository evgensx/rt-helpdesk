import asyncio
from os import getenv
import aio_pika
import aio_pika.abc as _abc
import logging
from app.model import Ticket as TicketModel
from app.schema import TicketIn


class AioPikaClient:
    @classmethod
    async def connect(cls):
        aioloop = asyncio.get_event_loop()
        # Start connection
        connection = await aio_pika.connect_robust(
            getenv('RABBIT_MQ_URL', 'amqp://guest:guest@localhost:5672/'), loop=aioloop)
        return connection

    @classmethod
    async def process_message(cls, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            parse_message = TicketIn.parse_raw(message.body).dict()
            # logging.info('[+]Me ssage from queue: %s', parse_message)
            await TicketModel.create(**parse_message)

    @classmethod
    async def consume(cls):
        try:
            connection: _abc.AbstractRobustConnection = await cls.connect()
        except Exception as e:
            logging.info('[+] Error: %s\n', e)
            await asyncio.sleep(15)
            await cls.consume()
        else:
            logging.info('[+] Connected to rabbitmq')
            # Creating channel
            channel: _abc.AbstractRobustChannel = await connection.channel(5)
            await channel.set_qos(10)
            # Declaring queue
            queue: _abc.AbstractRobustQueue = await channel.declare_queue(
                getenv('RABBIT_MQ_QUEUE', 'consume_queue'), durable=True)
            await queue.consume(cls.process_message, consumer_tag='servicedb')


    # async def publish(self, connection):
    #     pass


    @classmethod
    async def disconnect(cls):
        logging.info('[-] Disconnect from rabbitmq\n')
        connect: _abc.AbstractRobustConnection = cls.connect()
        await connect.close()
