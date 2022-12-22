import asyncio
from tornado import web
from tornado import httpclient
import logging

logging.basicConfig(level=logging.DEBUG)


async def f():
    client = httpclient.AsyncHTTPClient()
    # request = httpclient.HTTPRequest(url= , method="POST")
    try:
        response = await client.fetch("http://www.google.com")
    except Exception as e:
        print("Error: %s" % e)
    else:
        print(response.body)

class FormHandler(web.RequestHandler):
    def post(self):
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write({'success': True})
        decoded_body = self.request.body.decode()
        logging.info("Receive POST request body: %s", decoded_body)
        try:
            pass
        except Exception as e:
            logging.info("Ошибка! %s", e)
    def options(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')
        self.set_header("Content-Type", "text/html; charset=UTF-8")


async def main():
    app = web.Application([
        (r"/submit", FormHandler),
    ])
    app.listen(8080)
    logging.info('Starting tornado...\n')
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Stopping tornado...\n')
