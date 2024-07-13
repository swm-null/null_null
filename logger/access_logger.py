import logging, logging.handlers
import datetime
from utils.create_directory import create_directory

create_directory("./logs/access")

access_logger = logging.getLogger("uvicorn.access")
now = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
handler = logging.handlers.TimedRotatingFileHandler(f'./logs/access/access_log_{now}', when='midnight', interval=1, backupCount=7)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
access_logger.addHandler(handler)
