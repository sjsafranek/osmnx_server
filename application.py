import os.path
import json
import uuid
import pickle
import logging
import osmnx as ox
import networkx as nx
from tornado.web import Application

from handlers import *
import utils
from logger import Logger

ox.config(log_console=True, use_cache=True, log_level=logging.DEBUG, log_name=Logger.name)

class OSMGraph(object):
    def __init__(self, place):
        self.place = place

        _ghsh = utils.calculateMD5ForString(place)

        graph_file = os.path.join('cache', '{0}.graph.p'.format(_ghsh))
        edges_file = os.path.join('cache', '{0}.edges.p'.format(_ghsh))

        if os.path.exists( graph_file ):
            Logger.debug("Loading graph from cached file")
            self.Graph = pickle.load( open( graph_file, "rb" ) )
            self.Edges = pickle.load( open( edges_file, "rb" ) )

        else:
            log.debug("Building graph from osm data")
            self.Graph = ox.graph_from_place(self.place, network_type='drive', simplify=False)
            self.Edges = ox.graph_to_gdfs(self.Graph, nodes=False, edges=True)

            Logger.debug("Saving graph to cached file")
            pickle.dump( self.Graph, open( graph_file, "wb" ) )
            pickle.dump( self.Edges, open( edges_file, "wb" ) )

    def getClosestNode(self, longitude, latitude):
        point = (latitude, longitude)
        node = ox.get_nearest_node(self.Graph, point, return_dist=True)
        return node[0]

    def _findRoute(self, ll1, ll2):
        origin = self.getClosestNode(ll1['lng'], ll1['lat'])
        destination = self.getClosestNode(ll2['lng'], ll2['lat'])

        path = nx.shortest_path(self.Graph, origin, destination)

        features = [
            self.Edges.loc[ self.Edges['u'] == path[i] ].loc[ self.Edges['v'] == path[i+1] ]
            for i in range(len(path)-1)
        ]

        collection = []
        for feature in features:
            geojson = json.loads(feature.geometry.to_json())['features'][0]
            geojson['properties']['osmid']    = ';'.join([ str(x) for x in feature.osmid.tolist() ])
            geojson['properties']['length']   = feature.length.item()
            geojson['properties']['maxspeed'] = feature.maxspeed.item()
            geojson['properties']['name']     = feature.name.item()

            for prop in geojson['properties']:
                try:
                    if math.isnan(geojson['properties'][prop]):
                        geojson['properties'][prop] = None
                except:
                    pass

            del geojson['bbox']
            collection.append(geojson)

        featureCollection = {"type":"FeatureCollection","features":collection}

        return featureCollection


    def findRoute(self, waypoints=[]):
        _id = utils.calculateMD5ForString(json.dumps(waypoints))
        Logger.info('[{0}] Find shorest path for {1} waypoints'.format(_id, len(waypoints)))
        paths = [
            self._findRoute(
                waypoints[x-1],
                waypoints[x]
            ) for x in range(1, len(waypoints) )
        ]

        collection = []
        for path in paths:
            collection += path['features']

        Logger.debug('[{0}] Path contains {1} features'.format(_id, len(collection)))
        return {
            "type":"FeatureCollection",
            "features":collection
        }


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
