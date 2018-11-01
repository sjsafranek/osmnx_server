
import os
import json
import math
import multiprocessing
import tornado.gen
import tornado.web
from tornado.template import Loader
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import tornado.escape

from logger import Logger

from osm_graph import findRoute


class MapHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/html')
        tmpl = Loader(
                    os.path.dirname(os.path.realpath(__file__))
                ).load("templates/map.html").generate()
        self.write( tmpl )


class ApiBaseHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(
                    max_workers = multiprocessing.cpu_count()
                )

    def initialize(self, graph):
        self._graph = graph

    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                data = tornado.escape.json_decode(self.request.body)
                self.data = data
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request


    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.write_json(kwargs)

    def write_json(self, response):
        self.set_header('Content-Type', 'application/json')
        output = json.dumps(response)
        output = output.replace('NaN', 'null')
        self.write(output)
        self.finish()


class ApiRouteHandler(ApiBaseHandler):

    @run_on_executor
    def findRoute(self, waypoints=[]):
        # return self._graph.findRoute(waypoints)
        return findRoute(self._graph, waypoints)

    @tornado.web.asynchronous # this will be async
    @tornado.gen.coroutine # we will be using coroutines, with gen.Task
    def post(self):
        waypoints = self.data
        Logger.info("{0} waypoints in payload".format(len(waypoints)))

        results = yield self.findRoute(waypoints)
        self.write_json(
            results
        )
