import asyncio
import tornado.web
import logging
import pika
from pika.adapters.tornado_connection import TornadoConnection

logging.basicConfig(level=logging.INFO)

def send_message(message='Hello World!', queue="helpdesk_queue", exchange='amq.direct',
                 routing_key="helpdesk_routing_key"):
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(host='172.16.0.4', port=5672, virtual_host='helpdesk',
                                           credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True,
                                auto_delete=False, internal=False, passive=True)
    channel.queue_declare(queue=queue, durable=True, auto_delete=False)
    channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    connection.close()
    logging.info("Send message: %s", message)

class JsonHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write({'success': True})
        decoded_body = self.request.body.decode()
        logging.info("Receive POST request body: %s", decoded_body)
        try:
            send_message(message=decoded_body)
        except Exception as e:
            logging.info("Ошибка! %s", e)
    def options(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header("Content-Type", "text/html; charset=UTF-8")


async def main():
    app = tornado.web.Application([
        (r"/submit", JsonHandler),
    ])
    app.listen(8080)
    logging.info('Starting tornado...\n')
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Stopping tornado...\n')
