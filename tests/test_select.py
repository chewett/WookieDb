import unittest
import sys
sys.path.append("../")
from WookieDb import *
import unittest

class TestSelectStatements(unittest.TestCase):

    def setUp(self):
        self.db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")
        self.db.query("""CREATE TABLE `basic_test` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `intVar` int(11) DEFAULT NULL,
                        `charVar` varchar(45) DEFAULT NULL,
                         PRIMARY KEY (`id`)
                       ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")
        self.data = {"intVar": "123", "charVar": "testing"}
        self.db.query("INSERT INTO basic_test VALUES ('', 123, 'testing');")
        self.db.query("INSERT INTO basic_test VALUES ('', 123, 'testing');")
        self.db.query("INSERT INTO basic_test VALUES ('', 123, 'testing');")

    def tearDown(self):
        self.db.query("DROP TABLE basic_test")

    def testBasicSelect(self):
        res = self.db.select("basic_test", "*")
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertEqual(len(r), 3)

        self.db.query("INSERT INTO basic_test VALUES ('',123, 'testing');")

        res = self.db.select("basic_test", "*")
        self.assertEqual(len(res), 4)
        for r in res:
            self.assertEqual(len(r), 3)


if __name__ == "__main__":
    unittest.main()
