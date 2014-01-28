import MySQLdb

class WookieDb:

    """ This initilises the class and attempts to connect to the given server
        and the database
    """
    def __init__(self, host, user, password, db, select_type="nodict"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.debug_mode = False
        self.select_type = select_type
        self.connect()

    def connect(self):
        self.connection = MySQLdb.Connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
        self.cursor = self.connection.cursor()

    """ Performs a select query based on the table, fields and conditions  """
    def select(self, table, fields, condition=""):
        return self.query("SELECT " + fields + " FROM " + table
                          + " " + condition)

    """ Takes a dict representing a row and inserts it into the table """
    def insert(self, table, data):
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
        sql = ("UPDATE " + table + " SET ")

        to_update = list()

        for column, value in data.iteritems():
            to_update.append(column + " = '" + value + "'")

        sql += ", ".join(to_update)

        sql += " " + condition
        self.query(sql)

    def delete(self, table, condition=""):
        sql = "DELETE FROM " + table + " "  + condition + ";"
        self.query(sql)

    """ Returns the last autoincrement ID """
    def get_last_autoincrement(self):
        return self.cursor.lastrowid

    """ Performs the selected SQL and returns the result if there is one
        This will return either a list of tuples or dicts depending on the
        value of select_type.
    """
    def query(self, sql):
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
        self.connection.commit()

    def _execute(self, sql):
        if self.debug_mode is True:
            print "Running SQL:", sql
        try:
            self.cursor.execute(sql)
        except OperationalError as e:
            if e[0] == 2006: #Error is that mysql server has gone away, attempts to reconnet and then runs it again. If it fails again let it fail
                self.connect()
                self.cursor.execute(sql)
            else:
                raise

