from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title='HTCPCP Example',
    icon='coffee',
    dependencies=[
        PluginDependency('main')
    ],
)


def init():
    import client
    import main
