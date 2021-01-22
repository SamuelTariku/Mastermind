from Handlers.Handlers import *
from Handlers.Todo import *
from Database.DAL import Database

# Handle the inputs
if (__name__ == '__main__'):
    # Config DB
    # database and/or database list
    todoDatabase = Database("Todo")

    # TODO figure out how to add indexed assignement like dictionary(hashmaps)
    # I.E todoDatabase[todo] = todo
    # List of tables for those databases
    todoDatabase.addTable(indexName="todo",
                          tableName="todo")

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
    print()
    print("Press any key to continue")
    input()
