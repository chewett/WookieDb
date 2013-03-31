import unittest
import sys
sys.path.append("../")
from WookieDb import *
import unittest

class TestBasicCommands(unittest.TestCase):

    def setUp(self):
        self.db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")

    def testWorking(self):
        """checks if the object is creatable and localhost accessible"""
        assert True

    def testQuery(self):
        """checks if running a query works"""
        res = self.db.query("select 1")
        self.assertEqual(res[0][0], 1)

    def testCreateTable(self):
        tables = self.db.query("show tables")

        self.db.query("""CREATE TABLE `basic_test` (
                        `id` int(11) NOT NULL,
                        `intVar` int(11) DEFAULT NULL,
                        `charVar` varchar(45) DEFAULT NULL,
                         PRIMARY KEY (`id`)
                       ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")

        tables = self.db.query("show tables")
        self.assertTrue(("basic_test",) in tables)

        self.db.query("DROP TABLE basic_test")



class TestInsertStatements(unittest.TestCase):

    def setUp(self):
        self.db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")
        self.db.query("""CREATE TABLE `basic_test` (
                        `id` int(11) NOT NULL,
                        `intVar` int(11) DEFAULT NULL,
                        `charVar` varchar(45) DEFAULT NULL,
                         PRIMARY KEY (`id`)
                       ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")
        self.data = {"intVar": "123", "charVar": "testing"}

    def testOneInsert(self):
        res = self.db.query("select * from basic_test")
        self.assertEqual(len(res), 0)
        self.db.insert("test_basic", self.data)

        res = self.db.query("select * from basic_test")
        self.assertEqual(len(res), 1)

if __name__ == "__main__":
    unittest.main()
