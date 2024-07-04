import logging, logging.handlers
import datetime
import uvicorn.logging
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

createDirectory("./logs/debug")
createDirectory("./logs/access")

logger = logging.getLogger('uvicorn')
console_formatter = uvicorn.logging.ColourizedFormatter(
    "{asctime} - {message}",
    style="{", use_colors=True)
now = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
handler = logging.handlers.TimedRotatingFileHandler(f'./logs/debug/code_exec_log_{now}.log', when='midnight', interval=1, backupCount=1)
handler.setFormatter(console_formatter)
logger.addHandler(handler)
