'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from enum import Enum


class RPQRScannerStates(Enum):
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
