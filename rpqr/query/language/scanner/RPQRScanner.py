'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from enum import Enum
import logging
from typing import Optional, List

from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.scanner import RPQRToken


class States(Enum):
    """ States of scanners FSM.
    """
    START = 0
    AND = 1
    OR = 2
    NUMBER = 3
    COMMAND = 4
    STARTSTRING = 5
    STRINGCONTENT = 6
    ENDSTRING = 7
    LEFTBRACELET = 8
    RIGHTBRACELET = 9
    NOT = 10
    COMMA = 11


class RPQRScanner:
    """ Scanner of RPQR language.
    """
    def __init__(self, config: RPQRConfiguration) -> None:
        """ Create instance of RPQRScanner

        :param config: provided rpqr configuration
        :type config: RPQRConfiguration
        """
        self.tokenTypes = config.tokenTypes
        self.commandTypes = config.commandTypes
        self.allowedSpecialCharacters = config.allowedSpecialCharacters

    def getTokens(self, input: str) -> Optional[List[RPQRToken]]:
        """ Get RPQR language tokens from string

        :param input: input query
        :type input: str
        :return: list of RPQRToken objects
        :rtype: Optional[List[RPQRToken]]
        """
        tokens = []
        curToken = RPQRToken()
        curState = States.START
        curInputIndex = 0
        # typical FSM for scanning of input string
        while curInputIndex < len(input) + 1:
            if curInputIndex < len(input):
                c = input[curInputIndex]
            else:
                c = ''
            if curState == States.START:
                if c == '':
                    break
                elif c == '(':
                    curToken = RPQRToken(self.tokenTypes["leftBracelet"], c)
                    curState = States.LEFTBRACELET
                elif c == ')':
                    curToken = RPQRToken(self.tokenTypes["rightBracelet"], c)
                    curState = States.RIGHTBRACELET
                elif c == '&':
                    curToken = RPQRToken(self.tokenTypes["and"], c)
                    curState = States.AND
                elif c == '|':
                    curToken = RPQRToken(self.tokenTypes["or"], c)
                    curState = States.OR
                elif c == '\'':
                    curToken = RPQRToken(self.tokenTypes["string"], '')
                    curState = States.STARTSTRING
                elif c == '~':
                    curToken = RPQRToken(self.tokenTypes["not"], c)
                    curState = States.NOT
                elif c == ',':
                    curToken = RPQRToken(self.tokenTypes["comma"], c)
                    curState = States.COMMA
                elif c.isnumeric():
                    curToken = RPQRToken(self.tokenTypes["number"], c)
                    curState = States.NUMBER
                elif c.isalpha():
                    curToken = RPQRToken(self.tokenTypes["command"], c)
                    curState = States.COMMAND
                elif not c.isspace():
                    logging.error("Lexical error while reading new token near %s in column %s" % (
                        c, curInputIndex))
                    return None
                curInputIndex += 1
            elif curState == States.AND:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.OR:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.NUMBER:
                if c.isnumeric():
                    curToken.appendToContent(c)
                    curInputIndex += 1
                else:
                    tokens.append(curToken)
                    curState = States.START
            elif curState == States.COMMAND:
                if c.isalpha():
                    curToken.appendToContent(c)
                    curInputIndex += 1
                else:
                    if curToken.content not in self.commandTypes.keys():
                        logging.error(
                            "Lexical error command %s not implemented" % (curToken.content))
                        return None
                    curToken.type = self.commandTypes[curToken.content]
                    tokens.append(curToken)
                    curState = States.START
            elif curState == States.STARTSTRING:
                if c.isalnum() or c in self.allowedSpecialCharacters:
                    curToken.appendToContent(c)
                    curInputIndex += 1
                    curState = States.STRINGCONTENT
                elif c == '\'':
                    curState = States.ENDSTRING
                else:
                    logging.error("Lexical error while reading string literal near %s in column %s missing '" % (
                        c, curInputIndex))
                    return None
            elif curState == States.STRINGCONTENT:
                if c.isalnum() or c in self.allowedSpecialCharacters:
                    curToken.appendToContent(c)
                    curInputIndex += 1
                elif c == '\'':
                    curState = States.ENDSTRING
                else:
                    logging.error("Lexical error while reading string literal near %s in column %s missing '" % (
                        c, curInputIndex))
                    return None
            elif curState == States.ENDSTRING:
                tokens.append(curToken)
                curInputIndex += 1
                curState = States.START
            elif curState == States.LEFTBRACELET:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.RIGHTBRACELET:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.NOT:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.COMMA:
                tokens.append(curToken)
                curState = States.START
        tokens.append(RPQRToken(self.tokenTypes["end"]))
        return tokens
