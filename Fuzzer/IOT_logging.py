import logging

logger = logging.getLogger('fuzzer')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s', "%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)