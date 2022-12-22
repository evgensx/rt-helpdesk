import asyncio
from tornado import web
from tornado import httpclient
import logging


async def f():
    client = httpclient.AsyncHTTPClient()
    try:
        request = httpclient.HTTPRequest(url="http://localhost:15672/api/queues/helpdesk/helpdesk_queue/get", method="POST", auth_username='admin', auth_password='admin')
        response = await client.fetch("http://www.google.com")
    except Exception as e:
        print("Error: %s" % e)
    else:
        print(response.body)

async def main():
    await f()
    await asyncio.Event().wait()

asyncio.run(main())