""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.uid import generate_uid

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testgenerate_uid(self):
        self.assertEqual(8, len(generate_uid()))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
