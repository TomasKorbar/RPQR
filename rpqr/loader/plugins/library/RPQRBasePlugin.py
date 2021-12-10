import sqlite3
from typing import Type


class RPQRBasePlugin:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def _addColumn(self, type: Type, name: str):
        if type == str:
            self.connection.execute("ALTER TABLE PACKAGES ADD COLUMN %s TEXT" % name)
            self.connection.commit()

    def fillData(self, id, pkg):
        pass
    
    def prepareData(pkg):
        pass