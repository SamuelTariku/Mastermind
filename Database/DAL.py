import sqlite3


class DAL():

    def __init__(self, database, table):
        self.database = database
        self.databaseName = database
        self.table = table

     # ------- Connection Tests -----

    def runDatabaseTest(self):
        try:
            self.conn = sqlite3.connect(self.database)
        except sqlite3.OperationalError as e:
            print(e)
            print("DATABASE CONNECTION FAILED cannot find {databaseName}".format(
                databaseName=self.database))
            return False
        return True

    def runTableTest(self):
        try:
            self.conn.execute(
                "select * from {tableName}".format(tableName=self.table))
        except sqlite3.OperationalError:
            print("Cannot find table {tableName} in {databaseName}".format(
                tableName=self.table, databaseName=self.database))
            return False
        return True

    # close the database

    def closeDatabase(self):
        self.conn.close()


class Database():
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def addTable(self, indexName, tableName):
        self.tables[indexName] = tableName

    def getTable(self, indexName):
        return self.tables[indexName]

    def getName(self):
        return self.name
