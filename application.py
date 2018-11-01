import uuid
import logging
from tornado.web import Application

from handlers import *
from osm_graph import *
from logger import Logger

def MakeApp(place):
    Logger.debug("Creating app for {0}".format(place))

    geograph = OSMGraph(place)

    app = Application([
        (r"/map", MapHandler),
        (r"/api/v1/route", ApiRouteHandler, dict(graph = geograph) ),
    ], **{
        "cookie_secret": str(uuid.uuid4()),
        "xsrf_cookies": False,
        "debyg":True
    })

    return app
