
from .. import itoolkit

class _TransportBase:
    def toolkit(self):
        return itoolkit.iToolKit(transport=self)
