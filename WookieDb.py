'''
This is a wrapper class around MySQLdb to handle the connection and data
processing in a nicer way.
'''

import MySQLdb

class WookieDb:
    '''Wrapper for MySQLdb to handle MySQL connections nicer'''

    def __init__(self, host, user, password, db, select_type="nodict", charset=None):
        """ This initilises the class and attempts to connect to the given server
            and the database
        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.debug_mode = False
        self.print_sql_errors = False
        self.select_type = select_type
        self.charset = charset
        self.cursor = None #set up in connect method called next
        self.connection = None #set up in connect method called next
        self.connect()

    def connect(self):
        '''Connects to the database'''
        if self.charset is not None:
            self.connection = MySQLdb.Connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset=self.charset)
        else:
            self.connection = MySQLdb.Connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
        self.cursor = self.connection.cursor()

    def select(self, table, fields, condition=""):
        """ Performs a select query based on the table, fields and conditions  """
        return self.query("SELECT " + fields + " FROM " + table
                          + " " + condition)

    def insert(self, table, data):
        """ Takes a dict representing a row and inserts it into the table """
        data_keys = []
        data_values = []
        for key in data.keys():
            try:
                data_keys.append(key.encode('utf-8'))
            except AttributeError:
                data_keys.append(str(key))

        for value in data.values():
            try:
                data_values.append(value.encode('utf-8'))
            except AttributeError:
                data_values.append(str(value))


        sql = ("INSERT INTO " + table + "(" +
              ", ".join(data_keys) + ") VALUES (\"" +
              "\", \"".join(data_values) + "\");")

        self.query(sql)

    def update(self, table, data, condition=""):
        '''Allows updates based on a dict of data, conditions and table'''
        sql = ("UPDATE " + table + " SET ")

        to_update = list()

        for column, value in data.iteritems():
            to_update.append(column + " = '" + value + "'")

        sql += ", ".join(to_update)

        sql += " " + condition
        self.query(sql)

    def delete(self, table, condition=""):
        '''Allows you to delete based on a condition and table'''
        sql = "DELETE FROM " + table + " "  + condition + ";"
        self.query(sql)

    def get_last_autoincrement(self):
        """ Returns the last autoincrement ID """
        return self.cursor.lastrowid

    def query(self, sql):
        """ Performs the selected SQL and returns the result if there is one
            This will return either a list of tuples or dicts depending on the
            value of select_type.
        """
        if self.select_type == "dict":
            self._execute(sql)

            description = self.cursor.description
            results = self.cursor.fetchall()

            results_dict = list()
            for res in results:
                res_dict = dict()

                i = 0
                for res_part in res:
                    res_dict[description[i][0]] = res_part
                    i += 1

                results_dict.append(res_dict)

            return results_dict

        else:
            self._execute(sql)
            return self.cursor.fetchall()

    def commit(self):
        '''Commits the transactions to the database'''
        self.connection.commit()

    def _execute(self, sql):
        '''Executes the provided SQL and allows some debugging'''
        if self.debug_mode is True:
            print "Running SQL:", sql
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError as err:
            if err[0] == 2006: #Error is that mysql server has gone away, attempts to reconncet and then runs it again. If it fails again let it fail
                self.connect()
                self.cursor.execute(sql)
            else:
                if self.print_sql_errors:
                    print "SQL RUNNING: " + sql
                raise

