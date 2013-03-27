import MySQLdb

class WookieDb:

    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.Connect(host=host, user=user, passwd=password, db=db)
        self.cursor = self.connection.cursor()

    def select(self, table, fields, condition=None):
        raise NotImplementedError("Not yet implemented, planned for future")

    def insert(self, table, data):
        raise NotImplementedError("Not yet implemented, planned for future")

    def update(self, table, data, condition=None):
        raise NotImplementedError("Not yet implemented, planned for future")

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
