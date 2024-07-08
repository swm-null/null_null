import logging, logging.handlers
import datetime
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

createDirectory("./logs/access")

access_logger = logging.getLogger("uvicorn.access")
now = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
handler = logging.handlers.TimedRotatingFileHandler(f'./logs/access/access_log_{now}', when='midnight', interval=1, backupCount=7)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
access_logger.addHandler(handler)
