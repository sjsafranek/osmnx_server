import logging
import tornado.log

# set logging format
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = tornado.log.LogFormatter(
                            fmt="%(asctime)s %(color)s[%(levelname)s]%(end_color)s [%(threadName)s] %(filename)s %(funcName)s:%(lineno)d %(message)s",
                            color=True,
                            datefmt='%Y-%m-%d %H:%M:%S')
if 0 != len(logger.handlers):
    streamhandler = logger.handlers[0]
    streamhandler.setFormatter(formatter)
else:
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

Logger = tornado.log.app_log
