import logging, logging.handlers
import datetime
from utils.create_directory import create_directory

create_directory("./logs/access")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

now = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
handler = logging.handlers.TimedRotatingFileHandler(f'./logs/exec/exec_log_{now}', when='midnight', interval=1, backupCount=7)
logging.getLogger().addHandler(handler)
