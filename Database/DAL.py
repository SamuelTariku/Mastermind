import sqlite3


class DAL():

    def __init__(self, database, table):
        self.database = database + ".db"
        self.databaseName = database
        self.table = table


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
