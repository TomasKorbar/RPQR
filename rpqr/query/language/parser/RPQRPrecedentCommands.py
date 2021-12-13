from enum import Enum


class RPQRPrecedentCommands(Enum):
    LOADMORE = 0
    COLLAPSE = 1
    CONTINUE = 2
    ERROR = 3
    SUCCESS = 4
