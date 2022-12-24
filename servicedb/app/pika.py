import asyncio
import aio_pika
import aio_pika.abc as _abc
import logging


async def pika_client(loop):
    conn = await aio_pika.connect_robust(
        "amqp://admin:admin@rabbitmq:5672:/helpdesk", loop=loop)

    async with conn:
        # Init queue name
        queue_name = "tickets"
        # Creating channel
        channel: _abc.AbstractChannel = await conn.channel()
        # Declaring queue
        queue: _abc.AbstractQueue = await channel.declare_queue(queue_name)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                logging.info(message.body)

                if queue.name in message.body.decode():
                    break
