'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

class RPQRBasePlugin:
    implementedCommands = list()

    def fillData(self, id, pkg, graph):
        pass

    def prepareData(self):
        pass
