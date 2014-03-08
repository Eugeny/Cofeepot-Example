import requests

from ajenti.api import *
from ajenti.plugins.configurator.api import ClassConfigEditor


@plugin
class HTCPCPClientConfigEditor (ClassConfigEditor):
    """
    A plugin that handles editing of HTCPCPClient's classconfig
    """
    title = 'HTCPCP Client'
    icon = 'coffee'

    def init(self):
        self.append(self.ui.inflate('htcpcp:config'))  # htcpcp/layout/config.xml


class CoffeeAddition (object):
    def __init__(self, name):
        self.name = name
        self.selected = False


@plugin
class HTCPCPClient (BasePlugin):
    classconfig_editor = HTCPCPClientConfigEditor  # connect this plugin with a ConfigEditor
    default_classconfig = {'url': 'htcpcp://127.0.0.1:5000'}

    def init(self):
        self.additions = []

    def check_connectivity(self):
        resp = requests.request('PROPFIND', self.get_url())
        if resp.status_code == 418:
            raise Exception('This coffee pot is a teapot')

    def refresh(self):
        resp = requests.request('PROPFIND', self.get_url())
        self.additions = [CoffeeAddition(x) for x in resp.headers['Additions-List'].split(';')]

    def get_url(self):
        return self.classconfig['url'].replace('htcpcp', 'http')

    def brew(self):
        """
        Brew coffee with selected additions
        """
        return requests.request('BREW', self.get_url(), headers={
            'Accept-Additions': ';'.join(x.name for x in self.additions if x.selected)
        })

    def retrieve(self):
        return requests.request('GET', self.get_url())
