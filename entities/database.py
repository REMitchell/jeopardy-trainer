import pymysql
from pymysql.err import InternalError, InterfaceError, ProgrammingError

class Database:
    def __init__(self, database):
        self.database = database
        #Assumes port 3306
        self.conn = self.connection()
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("USE {}".format(self.database))

    def connection(self):
        return pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='root', db='mysql', charset='utf8')

    def execute(self, query, params=()):
        try:
            self.cur.execute(query, params)
        except InterfaceError:
            # Has been happening because the cursor closes
            print("INTERFACE ERROR")
            self.restart(query, params)
        except ProgrammingError:
            print("INTERFACE ERROR")
            self.restart(query, params)
    
    def restart(self, query, params):
            try:
                self.cur.close()
            except:
                pass
            try:
                self.conn.close()
            except:
                pass
            self.conn = self.connection()
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cur.execute("USE {}".format(self.database))
            self.execute(query, params)
        


