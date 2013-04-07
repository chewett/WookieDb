import unittest
import sys
sys.path.append("../")
from WookieDb import *

class TestUpdateStatements(unittest.TestCase):

    def setUp(self):
        self.db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")
        self.db.query("""CREATE TABLE `basic_test` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `intVar` int(11) DEFAULT NULL,
                        `charVar` varchar(45) DEFAULT NULL,
                         PRIMARY KEY (`id`)
                       ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")i
        self.data = {"intVar": "345", "charVar": "testing2"}
        self.db.query("INSERT INTO basic_test VALUES ('', 123, 'testing');")

    def tearDown(self):
        self.db.query("DROP TABLE basic_test")

    def testOneUpdate(self):
        res = self.db.query("select * from basic_test WHERE ID = 1")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][1], 123)
        self.assertEqual(res[0][2], "testing")

        self.update("basic_test", self.data, "WHERE ID = 1")

        res = self.db.query("select * from basic_test")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][1], 345)
        self.assertEqual(res[0][2], "testing2")

if __name__ == "__main__":
    unittest.main()
