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



#
# def log(log_name):
# 	# Set up a specific logger with our desired output level
# 	logger = logging.getLogger(log_name)
# 	# handler = logging.FileHandler(log_name+'.log')
# 	logger.setLevel(logging.DEBUG)
# 	ch = logging.StreamHandler()
# 	ch.setLevel(logging.DEBUG)
# 	# create formatter
# 	formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(filename)s line:%(lineno)d : %(message)s")
# 	# add formatter to ch
# 	handler.setFormatter(formatter)
# 	ch.setFormatter(formatter)
# 	# add ch to logger
# 	logger.addHandler(ch)
# 	logger.addHandler(handler)
# 	return logger
