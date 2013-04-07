import MySQLdb

class WookieDb:

    """ This initilises the class and attempts to connect to the given server
        and the database
    """
    def __init__(self, host, user, password, db, select_type="nodict"):
        self.connection = MySQLdb.Connect(host=host, user=user, passwd=password, db=db)
        self.cursor = self.connection.cursor()
        self.select_type = select_type

    """ Performs a select query based on the table, fields and conditions  """
    def select(self, table, fields, condition=""):
        return self.query("SELECT " + fields + " FROM " + table
                          + " " + condition)

    """ Takes a dict representing a row and inserts it into the table """
    def insert(self, table, data):
        sql = ("INSERT INTO " + table + "(" +
              ", ".join(map(str, data.keys())) + ") VALUES (\"" +
              "\", \"".join(map(str, data.values())) + "\");")

        self.query(sql)

    def update(self, table, data, condition=""):
        sql = ("UPDATE " + table + " SET ")

        to_update = list()

        for column, value in data.iteritems():
            to_update.append(column + " = '" + value + "'")

        sql += ", ".join(to_update)

        sql += " " + condition
        self.query(sql)

    """ Performs the selected SQL and returns the result if there is one
        This will return either a list of tuples or dicts depending on the
        value of select_type.
    """
    def query(self, sql):
        if self.select_type == "dict":
            self.cursor.execute(sql)

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
            self.cursor.execute(sql)
            return self.cursor.fetchall()
