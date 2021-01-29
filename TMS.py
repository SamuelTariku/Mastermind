from Handlers.Handlers import *
from Handlers.Todo import *
from Database.DAL import Database

import os

# Handle the inputs
if (__name__ == '__main__'):
    # Config DB
    # database and/or database list

    databaseName = "Todo.db"
    
    #
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, databaseName)
    # exit()

    todoDatabase = Database(db)

    # TODO figure out how to add indexed assignement like dictionary(hashmaps)
    # I.E todoDatabase[todo] = todo
    # List of tables for those databases
    todoDatabase.addTable(indexName="todo",
                          tableName="todo")

    todoDatabase.addTable(indexName="group",
                          tableName="group")

    # Handler functions
    todoHandler = TodoHandler(todoDatabase)

    inputHandler = InputHandler()
    inputHandler.addHandler('todo', todoHandler)

    while not inputHandler.isExit:
        command = input('>')
        command = command.strip()
        inputHandler.handle(command)

    # close database
    todoHandler.database.closeDatabase()

    print(" \n Press any key to continue \n")
