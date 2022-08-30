import logging

VERSION = '0.5.4'
DEBUG = True
logging.basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) >> %(module)s.%(funcName)s: %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO
)
