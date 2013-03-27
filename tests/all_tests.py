import unittest
import sys
sys.path.append("../")
from WookieDb import *
import unittest

class WookieDbTest(unittest.TestCase):

    def setUp(self):
        self.db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")

    def testWorking(self):
        """checks if the object is creatable and localhost accessible"""
        assert True

if __name__ == "__main__":
    unittest.main()
