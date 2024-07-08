import logging, logging.handlers
import datetime
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

createDirectory("./logs/exec")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

now = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
handler = logging.handlers.TimedRotatingFileHandler(f'./logs/exec/exec_log_{now}', when='midnight', interval=1, backupCount=7)
logging.getLogger().addHandler(handler)
