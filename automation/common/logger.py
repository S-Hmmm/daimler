import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time


file_path = r'D:\Work\automation\log'
if not os.path.exists(file_path):
    os.mkdir(file_path)
log_file = os.path.join(file_path, time.strftime('%Y%m%d') + '.log')


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')

    # 控制台handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel('ERROR')

    # 时间滚动文件handler
    file_handler = TimedRotatingFileHandler(filename=log_file, when='D', interval=1, backupCount=7)
    file_handler.setLevel('INFO')

    formatter = logging.Formatter('%(asctime)s - [%(filename)s --> line:%(lineno)d] - %(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
