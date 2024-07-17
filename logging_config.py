import logging


def _logger():
    file_name = "logs.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] - %(lineno)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(file_name),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = _logger()
