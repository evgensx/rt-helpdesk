from app.db import db, Engine
from fastapi import FastAPI


app = FastAPI(title="Async FastAPI ServiceDB")


@app.on_event('startup')
async def startup() -> None:
    await db.connect()
    await Engine.create_all()

@app.on_event("shutdown")
async def shutdown() -> None:
    await db.disconnect()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(pika_consumer(loop))
    # loop.close()
