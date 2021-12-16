'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''


class RPQRResultTree:
    """ Helper object for resolution of Abstract Syntactic Tree
    """

    def __init__(self, result, childResults) -> None:
        self.childResults = childResults
        self.result = result
