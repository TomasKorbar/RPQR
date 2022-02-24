'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''


class RPQRStackSymbol:
    """ Symbol on parser stack
    """

    def __init__(self, type: int, children: list = [], operator: str = None) -> None:
        """ Create instance of RPQRStackSymbol

        :param type: type of symbol
        :type type: int
        :param children: children of this symbol, defaults to []
        :type children: list, optional
        :param operator: operator of this symbol, defaults to None
        :type operator: str, optional
        """
        self.children = children
        self.operator = operator
        self.type = type

    def setChildren(self, children):
        """ set children of this symbol

        :param children: children
        :type children: object
        """
        self.children = children

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, RPQRStackSymbol):
            return False
        elif (__o.operator == self.operator
                and __o.type == self.type
                and __o.children == self.children):
                return True
        else:
            return False