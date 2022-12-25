from app.db import DbCli as db
from app.pika_cli import AioPikaClient as pika
from fastapi import FastAPI


app = FastAPI(title="Async FastAPI ServiceDB")


@app.on_event('startup')
async def startup() -> None:
    await db.connect()
    await pika.consume()

@app.on_event("shutdown")
async def shutdown() -> None:
    await db.disconnect()
    await pika.disconnect()