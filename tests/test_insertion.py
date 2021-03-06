import unittest
import sys
sys.path.append("../")
from WookieDb import *

class TestInsertStatements(unittest.TestCase):

    def setUp(self):
        self.db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")
        self.db.query("""CREATE TABLE `basic_test` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `intVar` int(11) DEFAULT NULL,
                        `charVar` varchar(45) DEFAULT NULL,
                         PRIMARY KEY (`id`)
                       ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")
        self.data = {"intVar": "123", "charVar": "testing"}

    def tearDown(self):
        self.db.query("DROP TABLE basic_test")

    def testOneInsert(self):
        res = self.db.query("select * from basic_test")
        self.assertEqual(len(res), 0)
        self.db.insert("basic_test", self.data)

        res = self.db.query("select * from basic_test")
        self.assertEqual(len(res), 1)

    def testManyInsert(self):

        for i in xrange(100):
            res = self.db.query("select * from basic_test")
            self.assertEqual(len(res), i)
            self.db.insert("basic_test", self.data)

if __name__ == "__main__":
    unittest.main()
