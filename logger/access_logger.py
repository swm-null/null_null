import logging, logging.handlers
from logger.utils.create_directory import create_directory

create_directory("./logs/access")

access_logger = logging.getLogger("uvicorn.access")
handler = logging.handlers.TimedRotatingFileHandler(
    filename=f'./logs/access/access_log',
    when='midnight', 
    interval=1, 
    backupCount=15
)
handler.suffix = '%Y%m%d'

handler.setFormatter(logging.Formatter(
  '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s'
))
access_logger.addHandler(handler)
