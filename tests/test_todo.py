import unittest
from Handlers.Todo import *
from Database.TodoData import *
from Database.DAL import Database


class TodoTests(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)

        self.database = Database("Todo")
        self.database.addTable("todo", "todo")

        self.todo = TodoHandler(self.database)

        self.parameters = [
            Parameter(parameterName="tName", singleDash="n",
                      doubleDash="name", isRequired=True),

            Parameter(parameterName="tType", singleDash="t",
                      doubleDash="type", isRequired=True),

            Parameter(parameterName="tRepeat", singleDash="r",
                      doubleDash="repeat", isRequired=True,
                      inputType="bool"),

            Parameter(parameterName="tPriority", singleDash="p",
                      doubleDash="priority", isRequired=False)
        ]

    def test_build_task(self):
        arguments = "-n{work on todo program} -t{normal} -r{no} -p{inu}"
        parsedParameters = parameterParse(arguments, self.parameters)
        builtTask = self.todo.buildTask(parsedParameters)

        taskName = builtTask.taskName
        taskType = builtTask.taskType
        taskRepeat = builtTask.taskRepeat
        taskPriority = builtTask.taskPriority

        self.assertTrue(set((taskName, taskType, taskRepeat, taskPriority)).issuperset((
            "work on todo program", 'normal', False, 'inu')))

    def test_todo_table(self):
        td = TodoData("Todo", "todo")
        self.assertTrue(td.runTableTest())

    def test_todo_database(self):
        td = TodoData("Todo", "todo")
        self.assertTrue(td.runDatabaseTest())


if __name__ == "__main__":
    unittest.main()
