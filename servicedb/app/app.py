from app.db import DbCli as db
import app.pika_cli as aiopika
from fastapi import FastAPI


app = FastAPI(title="Async FastAPI ServiceDB")


@app.on_event('startup')
async def startup() -> None:
    await db.connect()
    await aiopika.receiver()

@app.on_event("shutdown")
async def shutdown() -> None:
    await db.disconnect()
    await aiopika.disconnect()