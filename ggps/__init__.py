__author__ = 'cjoakim'
__version__ = '0.1.4'

VERSION = __version__

"""
ggps library
"""

from .trackpoint import Trackpoint
from .sax import BaseHandler
from .gpx_handler import GpxHandler
from .tcx_handler import TcxHandler
from .path_parser import PathHandler