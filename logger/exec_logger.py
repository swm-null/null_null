import logging, logging.handlers
from logger.utils.create_directory import create_directory

def init():
    create_directory("./logs/exec")

    logging.basicConfig(level=logging.INFO) 

    handler = logging.handlers.TimedRotatingFileHandler(
        filename=f'./logs/exec/exec_log', 
        when='midnight', 
        interval=1, 
        backupCount=15
    )
    handler.suffix = '%Y%m%d'
    logging.getLogger().addHandler(handler)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s'
    )
    handler.setFormatter(formatter)
