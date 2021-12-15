'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

class RPQRToken:
    def __init__(self, type : int = None, content : str = ""):
        self.type = type
        self.content = content

    def appendToContent(self, what : str):
        self.content += what