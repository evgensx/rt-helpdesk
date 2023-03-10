import asyncio
from re import sub
from tornado.web import RequestHandler, Application
from pika_cli import sender
from model import TicketIn, TicketOut
from pydantic import ValidationError
import json
import logging


logging.basicConfig(level=logging.INFO)


async def validate(message: bytes) -> dict:
    try:
        message_decoded = message.decode()
    except UnicodeDecodeError as e:
        message_decoded = message.decode('cp1251')

    try:
        message_dict: dict = json.loads(message_decoded)
        message_dict["tel"] = int(sub(r"\D", "", message_dict["tel"]))
        form_validation = TicketIn.parse_obj(message_dict)
        logging.info("[+] Validated form! : %s", form_validation)
        message_out = TicketOut.parse_obj(message_dict).json().encode('utf-8')
        logging.info('Message out = %s', message_out)
        await sender(message_out) # send message to rabbitmq
        return {'success': True}

    except ValidationError as e:
        logging.info("[-] Error is: %s", e)
        error_list = []
        for error in e.errors():
            if error['type'] == 'value_error.missing':
                error = error['loc'][0]
                error_list.append(error)
        logging.info("[-] Error list is: %s", error_list)
        result = {}
        result["success"] = False
        result["type_error"] = "content"
        result["missing required fields"] = error_list
        return result

    except ConnectionError:
        return {"success": False, "type_error": "service unavailable"}


class SubmitHandler(RequestHandler):
    # async def prepare(self):
    #     if self.request.headers['Content-Type'] == 'application/x-json':
    #         self.args = json_decode(self.request.body)

    async def options(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.set_status(200)

    # async def post(self):
    #     """
    #     curl -i -X POST --data '{"last_name":"Familiya","first_name":"Imya","patronymic_name":"Otchestvo","tel": "+7 (123) 456 78 90","request_text":"help me"}' http://localhost:8888/submit
    #     """
    #     data = json.loads(self.request.body) #.decode('cp1251')
    #     data["tel"] = int(sub(r"\D", "", data["tel"]))
    #     # print(data, type(data))
    #     json_data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    #     # Encode json_data to utf-8
    #     json_data_utf8 = json_data.encode('utf-8')
    #     print(json_data_utf8)
    #     self.set_header('Access-Control-Allow-Origin', '*')
    #     self.write(json_data_utf8)

    async def post(self):
        result = await validate(self.request.body)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header('Access-Control-Allow-Origin', '*')
        if result['success'] == False:
            if result['type_error'] == "content":
                self.set_status(400)
            else:
                self.set_status(503)
        json_data = json.dumps(result, separators=(',', ':'))
        self.write(json_data)





def make_app():
    return Application([
        (r"/submit", SubmitHandler),
    ], debug=True)


async def main():
    app = make_app()
    app.listen(8888)
    logging.info('Starting Tornado web server')
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Stopping tornado...\n')
        exit()
