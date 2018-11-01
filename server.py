'''

# Dependencies
sudo aptitude install python3-osmnx
sudo aptitude install python3-rtree
sudo aptitude install python3-numpy
sudo aptitude install python3-pandas
sudo aptitude install python3-geopandas
sudo aptitude install python3-tornado

# NetworkX
https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path

# Geo-Python: Network analysis in Python
https://automating-gis-processes.github.io/2017/lessons/L7/network-analysis.html
https://automating-gis-processes.github.io/2017/lessons/L7/network-analysis.html#saving-shortest-paths-to-disk

# OSMnx
https://geoffboeing.com/2016/11/osmnx-python-street-networks/
https://github.com/gboeing/osmnx
https://github.com/gboeing/osmnx-examples
https://osmnx.readthedocs.io/en/stable/osmnx.html

'''

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

try:
    from tornadouvloop import TornadoUvloop
except ImportError:
    pass


# parse command line
define('port', default=5555, help="Run on the given port", type=int)
define('place', default='', help="Place to build path finding graph", type=str)
options.parse_command_line()
if "" == options.place:
    raise ValueError("Place cannot be undefined")


if __name__ == '__main__':
    from logger import Logger
    import application

    app = application.MakeApp(options.place)
    app.listen(options.port)
    Logger.info("Magic happens on port: {0}".format(options.port))
    try:
        IOLoop.configure(TornadoUvloop)
    except NameError:
        pass
    IOLoop.current().start()
