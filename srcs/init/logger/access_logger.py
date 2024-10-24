import logging, logging.handlers
from init.logger.utils import create_directory

class EndpointHealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.args and len(record.args) >= 3:
            endpoint_name: str=str(record.args[2]) # type: ignore
            return endpoint_name!="/"
        return True

def init():
    create_directory("..../logs/access")

    access_logger = logging.getLogger("uvicorn.access")
    logging.getLogger("uvicorn.access").addFilter(EndpointHealthCheckFilter())
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=f'..../logs/access/access_log',
        when='midnight', 
        interval=1, 
        backupCount=15
    )
    handler.suffix = '%Y%m%d'

    handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s'
    ))
    access_logger.addHandler(handler)
