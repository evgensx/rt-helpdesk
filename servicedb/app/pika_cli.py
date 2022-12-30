import asyncio
from os import getenv
from aio_pika import connect, Connection, IncomingMessage, Channel, Queue
import logging
from app.model import Ticket as TicketModel
from app.schema import TicketIn


connection: Connection


async def create_connection():
    # Connection setup
    return await connect(
        getenv('RABBIT_MQ_URL', 'amqp://guest:guest@localhost:5672/'))


async def disconnect():
    logging.info('[-] Disconnect from rabbitmq\n')
    global connection
    await connection.close()


async def on_message(message: IncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    async with message.process():
        parse_message = TicketIn.parse_raw(message.body).dict()
        # logging.info('[+]Me ssage from queue: %s', parse_message)
        await TicketModel.create(**parse_message)


async def receiver():
    try:
        #Perform connection
        global connection
        connection = await create_connection()
    except Exception as e:
        logging.info('[-] Error: %s\n', e)
        await asyncio.sleep(15)
        await receiver()
    else:
        logging.info('[+] Connected to rabbitmq')
        # Creating channel
        channel: Channel = await connection.channel(5)
        # Set QoS
        await channel.set_qos(1)
        # Declaring queue
        queue: Queue = await channel.declare_queue(
            getenv('RABBIT_MQ_QUEUE', 'consume_queue'), durable=True)
        # Start listening the queue with name helpdesk_queue
        await queue.consume(on_message, consumer_tag='servicedb')
