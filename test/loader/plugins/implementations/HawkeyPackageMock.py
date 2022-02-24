'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''


class HawkeyPackageMock:
    def __init__(self):
        self.requires = [1, 2, 3]
        self.source_name = "one"

    def __str__(self) -> str:
        return self.source_name
