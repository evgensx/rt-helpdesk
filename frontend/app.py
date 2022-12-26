from flask import Flask, jsonify

app = Flask(__name__)


@app.get('/')
async def ping():
    return {'message': 'pong'}


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# import asyncio
# import tornado.web

# class StaticFileHandler(tornado.web.StaticFileHandler):
#     async def get(self, path: str, include_body: bool = True) -> None:
#         return await super().get(path, include_body)

# class StaticHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("index.html")

# def make_app():
#     return tornado.web.Application([
#         (r"/", StaticHandler),
#         (r"/(.*)", StaticFileHandler, {"path": "./"})
#     ],)

# async def main():
#     app = make_app()
#     app.listen(80)
#     await asyncio.Event().wait()

# if __name__ == "__main__":
#     asyncio.run(main())