import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from ai.database.connection import client as mongo_client
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from init.logger import *

def init(app: FastAPI):
    load_dotenv()

    # init loggers
    access_logger_init()
    exec_logger_init()
    
    sentry_init()
    app.add_middleware(SentryAsgiMiddleware)
    
    # init database
    try:
        mongo_client.client.admin.command('ping')
        logging.info(f"Pinged your deployment. You successfully connected to {mongo_client.DB_NAME}!")
    except Exception as e:
        logging.error(e)
