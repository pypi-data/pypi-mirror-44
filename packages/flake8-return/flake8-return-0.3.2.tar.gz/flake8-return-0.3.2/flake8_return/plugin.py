from flake8_plugin_utils import Plugin

from .visitors import ReturnVisitor

__version__ = '0.3.2'


class ReturnPlugin(Plugin):
    name = 'flake8-return'
    version = __version__
    visitors = [ReturnVisitor]
