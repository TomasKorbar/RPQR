'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''


class MockFilter:
    def run():
        return ["one", "two", "three"]


class HawkeyQueryMock:
    def filter(self, provides=None):
        return MockFilter
