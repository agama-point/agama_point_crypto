"""
DEBUG / INFO / WARNING
"""

import logging



__version__ = "0.2" # 2023/03


def logger_init(log_file='debug.log', console=False, fshort=False):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    if fshort:
        formatter = logging.Formatter('%(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.debug('-'*39)
    logger.debug('[Logger] logger_init | ver: ' + __version__)
    return logger
