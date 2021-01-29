import sqlite3


class DAL():

    def __init__(self, db):
        self.conn = None


# Handle the DALS for each table
class Database():
    def __init__(self, name):
        self.name = name
        self.tables = {}
        self.dals = {}

        self.conn = None

        self.isDatabase = self.runDatabaseTest()

        if(self.isDatabase):
            print("\n ... connected to database {databaseName} ... \n".format(
                databaseName=self.name.split("\\")[-1]))
        else:
            # sqlite creates database if it cants find a database
            print("Database cannot be found!")
            exit()

    def addTable(self, indexName, tableName):
        if(not self.runTableTest(tableName)):
            return

        self.tables[indexName] = tableName
        self.dals[tableName] = None

    def setDAL(self, indexName, dal):
        self.dals[self.tables[indexName]] = dal

    def getConn(self):
        return self.conn

    def isTable(self, indexName):
        test = True
        try:
            self.tables[indexName]
        except KeyError:
            test = False
        return test

    def getTable(self, indexName):
        return self.tables[indexName]

    def getName(self):
        return self.name

    def __getitem__(self, arg):
        return self.dals[self.tables[arg]]

    def __setitem__(self, arg, value):
        self.dals[self.tables[arg]] = value(self)

    # ------- Connection Tests -----

    def runDatabaseTest(self):
        try:
            self.conn = sqlite3.connect(self.name)
        except sqlite3.OperationalError as e:
            print(e)
            print("DATABASE CONNECTION FAILED cannot find {databaseName}".format(
                databaseName=self.name))
            return False
        return True

    def runTableTest(self, table):
        try:
            self.conn.execute(
                "select * from {tableName}".format(tableName=table))
        except sqlite3.OperationalError:
            print("Cannot find table {tableName} in {databaseName}".format(
                tableName=table, databaseName=self.name))
            return False
        return True

    # close the database

    def closeDatabase(self):
        self.conn.close()
