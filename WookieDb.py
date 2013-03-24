import MySQLdb

class WookieDb:

    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.Connect(host=host, user=user, passwd=password, db=db)
        self.cursor = self.connection.cursor()

