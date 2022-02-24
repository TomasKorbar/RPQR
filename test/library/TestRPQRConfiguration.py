'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.library.RPQRConfiguration import RPQRConfiguration


class TestRPQRConfiguration(unittest.TestCase):
    """ Test RPQRConfiguration class
    """

    def testInit(self):
        """ Test initialization
        """
        testConfig = RPQRConfiguration(
            ["./rpqr/loader/plugins/implementations"], [("test-repo", "/dummy/url")])

    def testIsAttributeSupported(self):
        """ Test isAttributeSupported method
        """
        testConfig = RPQRConfiguration(
            ["./rpqr/loader/plugins/implementations"], [("test-repo", "/dummy/url")])
        self.assertTrue(testConfig.isAttributeSupported(["name"]))
