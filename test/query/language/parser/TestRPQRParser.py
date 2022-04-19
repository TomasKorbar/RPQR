'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.query.language.parser import RPQRParser
from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.parser.RPQRStackSymbol import RPQRStackSymbol
from rpqr.query.language.scanner.RPQRToken import RPQRToken


class TestRPQRParser(unittest.TestCase):
    def testParserOne(self):
        config = RPQRConfiguration(
            ["./test/query/language/parser/mock_plugins"], [])
        parser = RPQRParser(config)
        mylist = [RPQRToken(config.commandTypes["DUMMY"], "DUMMY"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["end"], "")
                  ]

        structure = parser.parseTokens(mylist)
        mystruct = RPQRStackSymbol(
            16, [RPQRToken(13, "DUMMY"), RPQRToken(6, "argument")])
        self.assertEqual(structure, mystruct)

    def testParserTwo(self):
        config = RPQRConfiguration(
            ["./test/query/language/parser/mock_plugins"], [])
        parser = RPQRParser(config)
        mylist = [RPQRToken(config.commandTypes["DUMMY"], "DUMMY"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["and"], "&"),
                  RPQRToken(config.commandTypes["DUMMY"], "DUMMY"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument2"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["end"], "")
                  ]

        structure = parser.parseTokens(mylist)
        mystruct = RPQRStackSymbol(16, [RPQRStackSymbol(16, [RPQRToken(13, "DUMMY"), RPQRToken(
            6, "argument")]), RPQRStackSymbol(16, [RPQRToken(13, "DUMMY"), RPQRToken(6, "argument2")])], "&")
        self.assertEqual(structure, mystruct)

    def testSubstatementParsing(self):
        config = RPQRConfiguration(
            ["./test/query/language/parser/mock_plugins"], [])
        parser = RPQRParser(config)

        mylist = [RPQRToken(config.commandTypes["SUB"], "SUB"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.commandTypes["DUMMY"], "DUMMY"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["and"], "&"),
                  RPQRToken(config.commandTypes["DUMMY"], "DUMMY"),
                  RPQRToken(config.tokenTypes["leftBracelet"], "("),
                  RPQRToken(config.tokenTypes["string"], "argument2"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["rightBracelet"], ")"),
                  RPQRToken(config.tokenTypes["end"], ""),
                  ]

        structure = parser.parseTokens(mylist)
        mystruct = RPQRStackSymbol(16, [RPQRToken(15, "SUB"), RPQRStackSymbol(16, [RPQRStackSymbol(16, [RPQRToken(13, "DUMMY"), RPQRToken(
            6, "argument")]), RPQRStackSymbol(16, [RPQRToken(13, "DUMMY"), RPQRToken(6, "argument2")])], "&")])
        self.assertEqual(structure, mystruct)
