'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from enum import Enum


class RPQRPrecedentCommands(Enum):
    LOADMORE = 0
    COLLAPSE = 1
    CONTINUE = 2
    ERROR = 3
    SUCCESS = 4
