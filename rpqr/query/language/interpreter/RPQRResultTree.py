'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

class RPQRResultTree:
    def __init__(self, result, childResults):
        self.childResults = childResults
        self.result = result
