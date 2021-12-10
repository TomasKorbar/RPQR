import sqlite3
from typing import Type
from rpqr.loader.plugins.library import RPQRBasePlugin


class RPQRDataPlugin(RPQRBasePlugin):
    desiredType: Type = None
    desiredName: str = None

    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)
        self._addColumn(self.desiredType, self.desiredName)

    def fillData(self, id, pkg):
        data = self.prepareData(pkg)
        self.connection.execute("UPDATE PACKAGES SET %s = '%s' WHERE ID = %s" % (
            self.desiredName, data, id))
