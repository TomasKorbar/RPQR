'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import logging
from typing import Optional, List

from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.scanner import RPQRToken
from rpqr.query.language.scanner import RPQRScannerStates

class RPQRScanner:
    """ Scanner of RPQR language.
    """

    def __init__(self, config: RPQRConfiguration) -> None:
        """ Create instance of RPQRScanner

        :param config: provided rpqr configuration
        :type config: RPQRConfiguration
        """
        self.logger = config.rootLogger.getChild("RPQRScanner")
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
        curState = RPQRScannerStates.START
        curInputIndex = 0
        # typical FSM for scanning of input string
        while curInputIndex < len(input) + 1:
            if curInputIndex < len(input):
                c = input[curInputIndex]
            else:
                c = ''
            if curState == RPQRScannerStates.START:
                if c == '':
                    break
                elif c == '(':
                    curToken = RPQRToken(self.tokenTypes["leftBracelet"], c)
                    curState = RPQRScannerStates.LEFTBRACELET
                elif c == ')':
                    curToken = RPQRToken(self.tokenTypes["rightBracelet"], c)
                    curState = RPQRScannerStates.RIGHTBRACELET
                elif c == '&':
                    curToken = RPQRToken(self.tokenTypes["and"], c)
                    curState = RPQRScannerStates.AND
                elif c == '|':
                    curToken = RPQRToken(self.tokenTypes["or"], c)
                    curState = RPQRScannerStates.OR
                elif c == '\'':
                    curToken = RPQRToken(self.tokenTypes["string"], '')
                    curState = RPQRScannerStates.STARTSTRING
                elif c == '~':
                    curToken = RPQRToken(self.tokenTypes["not"], c)
                    curState = RPQRScannerStates.NOT
                elif c == ',':
                    curToken = RPQRToken(self.tokenTypes["comma"], c)
                    curState = RPQRScannerStates.COMMA
                elif c.isnumeric():
                    curToken = RPQRToken(self.tokenTypes["number"], c)
                    curState = RPQRScannerStates.NUMBER
                elif c.isalpha():
                    curToken = RPQRToken(self.tokenTypes["command"], c)
                    curState = RPQRScannerStates.COMMAND
                elif not c.isspace():
                    logging.error("Lexical error while reading new token near %s in column %s" % (
                        c, curInputIndex))
                    return None
                curInputIndex += 1
            elif curState == RPQRScannerStates.AND:
                tokens.append(curToken)
                curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.OR:
                tokens.append(curToken)
                curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.NUMBER:
                if c.isnumeric():
                    curToken.appendToContent(c)
                    curInputIndex += 1
                else:
                    tokens.append(curToken)
                    curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.COMMAND:
                if c.isalpha():
                    curToken.appendToContent(c)
                    curInputIndex += 1
                else:
                    if curToken.content not in self.commandTypes.keys():
                        self.logger.error(
                            "Lexical error command %s not implemented" % (curToken.content))
                        return None
                    curToken.type = self.commandTypes[curToken.content]
                    tokens.append(curToken)
                    curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.STARTSTRING:
                if c.isalnum() or c in self.allowedSpecialCharacters:
                    curToken.appendToContent(c)
                    curInputIndex += 1
                    curState = RPQRScannerStates.STRINGCONTENT
                elif c == '\'':
                    curState = RPQRScannerStates.ENDSTRING
                else:
                    self.logger.error("Lexical error while reading string literal near %s in column %s missing '" % (
                        c, curInputIndex))
                    return None
            elif curState == RPQRScannerStates.STRINGCONTENT:
                if c.isalnum() or c in self.allowedSpecialCharacters:
                    curToken.appendToContent(c)
                    curInputIndex += 1
                elif c == '\'':
                    curState = RPQRScannerStates.ENDSTRING
                else:
                    self.logger.error("Lexical error while reading string literal near %s in column %s missing '" % (
                        c, curInputIndex))
                    return None
            elif curState == RPQRScannerStates.ENDSTRING:
                tokens.append(curToken)
                curInputIndex += 1
                curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.LEFTBRACELET:
                tokens.append(curToken)
                curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.RIGHTBRACELET:
                tokens.append(curToken)
                curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.NOT:
                tokens.append(curToken)
                curState = RPQRScannerStates.START
            elif curState == RPQRScannerStates.COMMA:
                tokens.append(curToken)
                curState = RPQRScannerStates.START
        tokens.append(RPQRToken(self.tokenTypes["end"]))
        return tokens
