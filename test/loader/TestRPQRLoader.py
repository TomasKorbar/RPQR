'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.loader.RPQRLoader import RPQRLoader

class TestRPQRLoader(unittest.TestCase):
    """ test RPQRLoader class
    """

    def testCreateDatabase(self):
        config = RPQRConfiguration(["./test/query/language/parser/mock_plugins"], [("test-repo", "https://tkorbar.fedorapeople.org/rpqrTestingRepo/")])        
        loader = RPQRLoader(config)
        self.assertEqual(len(loader.createDatabase().nodes), 1)
