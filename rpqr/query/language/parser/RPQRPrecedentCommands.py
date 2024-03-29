'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from enum import Enum


class RPQRPrecedentCommands(Enum):
    """Commands controlling precedence actions
    """
    LOADMORE = 0
    COLLAPSE = 1
    CONTINUE = 2
    ERROR = 3
    SUCCESS = 4
