'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.scanner.RPQRScanner import RPQRScanner
from rpqr.query.language.scanner.RPQRToken import RPQRToken


class TestRPQRScanner(unittest.TestCase):
    def testGetTokens(self):
        RPQRConfiguration._initializePlugins = lambda x: None
        config = RPQRConfiguration([], [])
        config.commandTypes = {
            "COMMANDONE": config.commandIndex, "COMMANDTWO": config.commandIndex+1}
        scanner = RPQRScanner(config)
        mylist = [RPQRToken(config.commandTypes["COMMANDONE"], "COMMANDONE"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["end"], "")
                  ]

        self.assertEqual(mylist, scanner.getTokens("COMMANDONE('argument')"))

    def testGetTokens2(self):
        RPQRConfiguration._initializePlugins = lambda x: None
        config = RPQRConfiguration([], [])
        config.commandTypes = {
            "COMMANDONE": config.commandIndex, "COMMANDTWO": config.commandIndex+1}
        scanner = RPQRScanner(config)
        mylist = [RPQRToken(config.commandTypes["COMMANDONE"], "COMMANDONE"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["or"], "|"),
                  RPQRToken(config.commandTypes["COMMANDTWO"], "COMMANDTWO"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["number"], "3"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["end"], "")
                  ]

        self.assertEqual(mylist, scanner.getTokens("COMMANDONE('argument') | COMMANDTWO(3)"))
