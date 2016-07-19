import subprocess
import os
import tempfile

class MysqldumpWrapper:
    '''wrapper for mysqldump to'''

    MYSQL_DUMP_LOCATIONS = [
        "mysqldump"
    ]

    MYSQL_DUMP_LOCATION = False

    def __init__(self):
        self.__populate_mysql_dump_locations()
        self.__find_mysql_dump()

    def __find_mysql_dump(self):
        for loc in self.MYSQL_DUMP_LOCATIONS:
            result = self.__check_mysql_dump_exists_here(loc)
            if result is not False:
                self.MYSQL_DUMP_LOCATION = '"' + loc + '"'
                return

    def __populate_mysql_dump_locations(self):
        windows_dirs_to_check = [
            "C:\\Program Files\\MySQL\\",
            "C:\\Program Files (x86)\\MySQL\\"
        ]

        for directory in windows_dirs_to_check:
            if os.path.isdir(directory):
                for dir in os.listdir(directory):
                    possible_location = os.path.join(directory, dir, "bin", "mysqldump.exe")
                    if "Server" in dir and os.path.isfile(possible_location):
                        self.MYSQL_DUMP_LOCATIONS.append(possible_location)

    def __check_mysql_dump_exists_here(self, path):
        try:
            output = subprocess.check_output([path, "--version"])
            return output
        except Exception as e:
            return False

    def dump_tables_to_file(self, hostname, user, password, schema, tables, backup_location):
        if self.MYSQL_DUMP_LOCATION is False:
            raise Exception("Cannot find mysqldump so not executing")

        # set up the cnf file to dump
        tmpfile, tmpfile_path = tempfile.mkstemp(suffix=".my.cnf")
        table_files = []
        with open(tmpfile_path, 'w') as tmpfile_file:
            tmpfile_file.writelines(["[mysqldump]\r\n", 'password="' + password + '"'])

        for table in tables:
            table_file = os.path.join(backup_location, table + ".sql")
            command = self.MYSQL_DUMP_LOCATION + ' --defaults-file=' + tmpfile_path + ' --host=' + hostname + ' --protocol=tcp --user=' + user \
                      + ' --lock-tables=FALSE --compress=TRUE --port=3306 --default-character-set=utf8 --skip-triggers "' + \
                      schema + '" "' + table + '" > "' + table_file + '"'
            print command
            subprocess.call(command, shell=True)

            table_files.append(table_file)

        os.unlink(tmpfile_path)

        return table_files