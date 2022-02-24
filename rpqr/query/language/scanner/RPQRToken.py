'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''


class RPQRToken:
    """ RPQR Language token
    """

    def __init__(self, type: int = None, content: str = "") -> None:
        """ Create instance of RPQRToken

        :param type: type of token, defaults to None
        :type type: int, optional
        :param content: data contained in this token, defaults to ""
        :type content: str, optional
        """
        self.type = type
        self.content = content

    def appendToContent(self, what: str):
        """ Add data to content

        :param what: data
        :type what: str
        """
        self.content += what

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, RPQRToken):
            return False
        return True if self.type == __o.type and self.content == __o.content else False
