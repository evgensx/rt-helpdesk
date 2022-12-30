import asyncio
from tornado.web import RequestHandler, Application
from pika_cli import sender
from model import TicketIn, TicketOut
from pydantic import ValidationError
import logging

logging.basicConfig(level=logging.INFO)

async def to_rabbit(message):
    await sender(message)

async def validate(message: bytes) -> dict:
    try:
        form_validation = TicketIn.parse_raw(message) # декодируем форму
        logging.info("[+] Validated form! : %s", form_validation)
        message_out = TicketOut.parse_raw(message).json().encode('utf-8')
        logging.info('Message out = %s', message_out)
        await to_rabbit(message_out)
        return {'success': True}
    except ValidationError as e:
        # print(e)
        error_list = []
        for error in e.errors():
            if error['type'] == 'value_error.missing':
                error = error['loc'][0]
                error_list.append(error)
        logging.info("[-] Error list is: %s", error_list)
        result: dict[str, list | bool] = {'success': False}
        result['missing required fields'] = error_list
        return result
    except ConnectionError:
        return {'success': False, 'connection': False, 'solution': 'please try later'}

class SubmitHandler(RequestHandler):
    async def post(self):
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        form_body = self.request.body
        self.write(await validate(form_body))

    def options(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header("Content-Type", "text/html; charset=UTF-8")


async def main():
    app = Application([
        (r"/submit", SubmitHandler),
    ], autoreload=True, debug=True)
    app.listen(8080)
    logging.info('Starting tornado...\n')
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Stopping tornado...\n')
