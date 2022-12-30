from os import getenv
from aio_pika import connect_robust, Message
import logging


async def create_connection():
    # Connection setup
    return await connect_robust(
        getenv('RABBIT_MQ_URL', 'amqp://guest:guest@localhost:5672/'))


async def sender(message: bytes):
    #Perform connection
    async with await create_connection() as connection:
        # Creating a channel
        channel = await connection.channel(1)
        logging.info('[+] Connect to rabbitmq\n')

        # Declaring exchange
        exchange = await channel.declare_exchange(
            getenv('RABBIT_MQ_EXCHANGE', 'amq.direct'), durable=True
        )

        # Declaring queue
        queue = await channel.declare_queue(
            getenv('RABBIT_MQ_QUEUE', 'consume_queue'), durable=True
        )
        await queue.bind(exchange, getenv('RABBIT_MQ_ROUTING_KEY'))

        # Sending the message
        await exchange.publish(
            Message(message), routing_key=getenv('RABBIT_MQ_ROUTING_KEY', 'key')
        )

        logging.info('[-] Disconnect from rabbitmq\n')
