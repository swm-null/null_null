from dotenv import load_dotenv
from fastapi import FastAPI
from logger import access_logger, exec_logger, sentry_init
from ai.database.connection import client as mongo_client
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

def init(app: FastAPI):
    load_dotenv()

    # init database
    try:
        mongo_client.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # init loggers
    access_logger.init()
    exec_logger.init()
    sentry_init.init()
    app.add_middleware(SentryAsgiMiddleware)
