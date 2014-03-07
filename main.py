from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder

from client import HTCPCPClient


@plugin
class CoffeePlugin (SectionPlugin):
    def init(self):
        self.title = 'Coffeepot'
        self.icon = 'coffee'
        self.category = _('System')

        self.append(self.ui.inflate('htcpcp:main'))
        self.pot = HTCPCPClient.get()
        self.binder = Binder(self.pot, self.find('pot-root'))

    def on_page_load(self):
        try:
            self.pot.check_connectivity()
        except Exception, e:
            self.context.notify('error', 'Could not access the coffee pot: %s!' % str(e))
            self.context.launch('configure-plugin', plugin=self.pot)
        
        if not self.pot.additions:
            self.pot.refresh()
            self.binder.populate()

    @on('brew', 'click')
    def on_brew(self):
        self.binder.update()
        resp = self.pot.brew()
        if resp.status_code == 200:
            self.context.notify('info', 'Brewing')
        else:
            self.context.notify('error', resp.text)

    @on('refresh', 'click')
    def on_refresh(self):
        self.pot.refresh()
        self.binder.populate()

    @on('retrieve', 'click')
    def on_retrieve(self):
        resp = self.pot.retrieve()
        if resp.status_code == 200:
            self.context.notify('info', resp.text)
        else:
            self.context.notify('error', resp.text)
