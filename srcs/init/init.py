import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from ai.utils.database.connection import client as mongo_client, DB_NAME
from init.logger import *

def init(app: FastAPI):
    # init loggers
    access_logger_init()
    exec_logger_init()
    sentry_init()
    app.add_middleware(SentryAsgiMiddleware)
    
    logging.info(f"Using .env file: {load_dotenv()}")
    
    # init database
    try:
        mongo_client.admin.command("ping")
        logging.info(f"You successfully connected to {DB_NAME}!")
    except Exception as e:
        logging.error(e)
