from Handlers.Handlers import *
from utils.utilities import *
from utils.tableFormat import *
from Database.TodoData import TodoData
from Models.Task import *


class TodoHandler(Handler):

    def __init__(self, db):
        self.commands = {
            "default": None,
            "create": {
                "default": None,
                "help": "Create a todo list",
                "task": self.commandNewTask
            },

            "newtask": self.commandNewTask,

            "show": {
                "default": self.commandShow,
                "help": "Displays tasks in todo list",
                "all": self.commandShowAll,
                "sort": self.commandShowSort
            },

            "clear": {
                "default": self.commandClear,
                "help": "Deletes tasks in todo list",
                "all": self.commandClearAll
            },

            "delete": {
                "default": self.commandClear,
                "help": "Deletes tasks in todo list",
                "all": self.commandClearAll
            },

            "modify": {
                "default": None,
                "help": "Modifies tasks in todo list",
                "task": self.commandModifyTask
            },

            "mod": {
                "default": None,
                "help": "Modifies tasks in todo list",
                "task": self.commandModifyTask
            },

            "help": {
                "default": "Create a todo list",
                "more": self.help,
                "help": "to see more detailed help type: todo help more"
            }
        }
        todoDatabase = db.getName()
        todoTable = db.getTable("todo")
        self.database = TodoData(todoDatabase, todoTable)

    def searchParameterList(self, name, parameterList):
        for parameter in parameterList:
            if(parameter.getName() == name):
                return parameter

        return None

    def buildModTask(self, parameters):

        taskID = None

        taskName = None
        taskType = None
        taskRepeat = None
        taskPriority = None

        # Get values
        for parameter in parameters:
            if (parameter.getName() == "tName"):
                taskName = parameter.getValue()
            elif (parameter.getName() == "tType"):
                taskType = parameter.getValue()
            elif (parameter.getName() == "tRepeat"):
                taskRepeat = parameter.getValue()
            elif (parameter.getName() == "tPriority"):
                taskPriority = parameter.getValue()
            elif (parameter.getName() == "tID"):
                taskID = parameter.getValue()
            else:
                pass

        # Send to taskbuilder
        newModTask = TaskBuilder.buildMod(
            taskName=taskName,
            taskType=taskType,
            taskRepeat=taskRepeat,
            taskPriority=taskPriority,
            taskID=taskID
        )

        return newModTask

    def buildTask(self, parameters):
        # Required Parameters
        taskName = None
        taskType = None
        taskRepeat = None

        # Optional Parameters
        taskPriority = None

        # Get values
        for parameter in parameters:
            if (parameter.getName() == "tName"):
                taskName = parameter.getValue()
            elif (parameter.getName() == "tType"):
                taskType = parameter.getValue()
            elif (parameter.getName() == "tRepeat"):
                taskRepeat = parameter.getValue()
            elif (parameter.getName() == "tPriority"):
                taskPriority = parameter.getValue()
            else:
                pass

        # Check if there are blanks
        if (None in (taskName, taskType, taskRepeat)):
            print("!!! Required parameters not found !!!")
            return

        newTask = TaskBuilder.build(
            taskName=taskName,
            taskType=taskType,
            taskRepeat=taskRepeat,
            taskPriority=taskPriority
        )

        return newTask

    def printList(self, tasks):
        # TABLE VIEW
        fields = [Task.configParameters['id']['field']] + \
            Task.configParameters['required']['fields'] + \
            Task.configParameters['optional']['fields']

        tableView = Table(fields)

        for task in tasks:
            data = []

            data.append(Task.__getattribute__(
                task, Task.configParameters['id']['attribute']))
            for attribute in Task.configParameters['required']['attributes']:
                data.append(Task.__getattribute__(task, attribute))

            for attribute in Task.configParameters['optional']['attributes']:
                data.append(Task.__getattribute__(task, attribute))
            tableView.addRow(data)

        print(tableView)

    @staticmethod
    def taskTypeValidation(value):
        normalTasks = ['normal', 'n']
        generalTasks = ['general', 'g']
        typeValue = None
        if(value.lower() in normalTasks):
            typeValue = 'normal'
        elif(value.lower() in generalTasks):
            typeValue = 'general'
        else:
            print("!!! {} is not a valid task type".format(value))
        return typeValue

    @staticmethod
    def taskPriorityValidation(value):
        # priority matrices
        ImportantUrgent = ['iu', 'ui', 'important urgent',
                           'urgent important', 'quick-wins', 'do first']
        ImporantNotUrgent = ['inu', 'nui', 'important not urgent',
                             'not urgent important', 'major-work', 'schedule']
        NotImportantUrgent = ['niu', 'uni', 'not important urgent',
                              'urgent not important', 'thankless', 'delegate']
        NotImportantNotUrgent = [
            'ninu', 'nuni', 'not important not urgent', 'not urgent not important', 'fill-ins', 'aviod']
        priorityValue = None
        if(value.lower() in ImportantUrgent):
            priorityValue = 'iu'
        elif(value.lower() in ImporantNotUrgent):
            priorityValue = 'inu'
        elif(value.lower() in NotImportantUrgent):
            priorityValue = 'niu'
        elif(value.lower() in NotImportantNotUrgent):
            priorityValue = 'ninu'
        else:
            print("!!! {} is not a valid task priority !!!".format(value))
        return priorityValue

    # --------- Insert task into data -------

    def commandNewTask(self, extra=None):
        # DOCSTRING FOR HELP
        """
        Creates a new task

        Usage: 
            "todo newtask -n{TASKNAME} -t{normal/general} -r{yes/no}"
                    OR
            "todo newtask --name{TASKNAME} --type{normal/general} --repeat{yes/no}


        Required Parameters:
            (-n  / --name) --------- Task name

            (-t / --type)  --------- Type of tasks.
                                        -general tasks are tasks that are 
                                        broad encompassing i.e WORK 
                                        or HYGINE.Tasks that can have subtasks

                                        -normal tasks are tasks that are
                                        specific and cant be broken down further
                                        i.e "work on css code" or "debug line 42"

            (-r / --repeat) ---------- Is this a recurring task?

        Optional Parameters:
            (-p / --priority) --------- Task priority based on priority matrix
                                        -important urgent (IU)
                                        -important not urgent (INU)
                                        -not important urgent (NIU)
                                        -not important not urgent (NINU)
        """
        if(extra == None):
            print("Extra was none")
            return

        # Merge extra together
        extraMerge = " ".join(extra)

        # list of input parameters
        parameters = [
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
        # ------  Custom Validation Functions ---------
        # Task Type Validation

        self.searchParameterList("tType", parameters).setCustomValidation(
            TodoHandler.taskTypeValidation
        )
        # Task Priority Validation

        self.searchParameterList("tPriority", parameters).setCustomValidation(
            TodoHandler.taskPriorityValidation
        )
        # ------------------------------------------------

        # if there are no inputs
        if (len(extraMerge) == 0):
            parsedParameters = []
        else:
            # Handle multi line input
            extraMerge = InputHandler.multilineInput(
                extraMerge, "todo newtask")

            # parse the arguments for the parameters
            parsedParameters = parameterParse(extraMerge, parameters)

            if (parsedParameters == None):
                print("!!! Task not created !!!")
                return

        # Check if required parameters are set
        parsedParameters = checkRequiredParameters(
            parameters, parsedParameters)

        # validate parameters get a task object
        builtTask = self.buildTask(parsedParameters)

        if (builtTask == None):
            print("\n ...Task not created... \n")
            return
        self.database.insertData(builtTask)

    # ------- Task modification for existing tasks ---
    def commandModifyTask(self, extra=None):
        """

        Change task parameters on todo list

        Usage:
            todo mod task --id{TASK ID} [-PARAMETER{PARAMETER TEXT},...] OR
            todo modify task --id{TASK ID} [-PARAMETER{PARAMETER TEXT},...]
        I.E:
            todo mod task --id{2} -n{work on todo list} -t{normal}


        Parameters:
            (-i / --id) ----------- Task id assigned to the task
            (-n  / --name) --------- Task name

            (-t / --type)  --------- Type of tasks.
                                        -general tasks are tasks that are 
                                        broad encompassing i.e WORK 
                                        or HYGINE. Tasks that can have subtasks

                                        -normal tasks are tasks that are
                                        specific and cant be broken down further
                                        i.e "work on css code" or "debug line 42"

            (-r / --repeat) ---------- Is this a recurring task?

            (-p / --priority) --------- Task priority based on priority matrix
                                        -important urgent (IU)
                                        -important not urgent (INU)
                                        -not important urgent (NIU)
                                        -not important not urgent (NINU)
        """
        if(extra == None):
            print("Extra was none")
            return

        # Merge extra together
        extraMerge = " ".join(extra)

        parameters = [
            Parameter(parameterName="tID", singleDash="i",
                      doubleDash="id", isRequired=True,
                      inputType="int"),

            Parameter(parameterName="tName", singleDash="n",
                      doubleDash="name", isRequired=False),

            Parameter(parameterName="tType", singleDash="t",
                      doubleDash="type", isRequired=False),

            Parameter(parameterName="tRepeat", singleDash="r",
                      doubleDash="repeat", isRequired=False,
                      inputType="bool"),

            Parameter(parameterName="tPriority", singleDash="p",
                      doubleDash="priority", isRequired=False)
        ]

        # ------  Custom Validation Functions ---------
        # Task Type Validation

        self.searchParameterList("tType", parameters).setCustomValidation(
            TodoHandler.taskTypeValidation
        )
        # Task Priority Validation

        self.searchParameterList("tPriority", parameters).setCustomValidation(
            TodoHandler.taskPriorityValidation
        )
        # ------------------------------------------------

        # if there are no inputs
        if (len(extraMerge) == 0):
            print("\n !!! No parameters entered !!! \n")
            return
        else:
            # Handle multi line input
            extraMerge = InputHandler.multilineInput(
                extraMerge, "todo modtask")

            # parse the arguments for the parameters
            parsedParameters = parameterParse(extraMerge, parameters)

            if (parsedParameters == None):
                print("\n !!! TASK NOT MODIFIED !!! \n")
                return

        # Check if required parameters are set
        parsedParameters = checkRequiredParameters(
            parameters, parsedParameters)

        # Build a modifier task
        builtModTask = self.buildModTask(parsedParameters)

        if (builtModTask == None):
            print("\n ...Task is not modified... \n")
            return

        self.database.updateByID(builtModTask.getTaskID(), builtModTask)

    # -------- Deleting tasks from database -----
    # delete all tasks
    def commandClearAll(self, extra):
        """
        Clears all tasks from todo list

        Usage:
            todo clear all

        """
        self.database.clearAllTasks()

    # delete one task by parameter
    def commandClear(self, extra):
        if(extra == None):
            print("Extra was none")
            return

        if(len(extra) == 0):
            print("\n ... There needs to be atleast one parameter .. \n")
            return

        # Merge extra together
        extraMerge = " ".join(extra)

        # TODO optimize parameters for handling changes
        parameters = [
            Parameter(parameterName="tID", singleDash="i",
                      doubleDash="id", isRequired=False,
                      inputType="int"),

            Parameter(parameterName="tName", singleDash="n",
                      doubleDash="name", isRequired=False),
        ]

        # Handle multi line input
        extraMerge = InputHandler.multilineInput(
            extraMerge, "todo delete task")

        # parse the arguments for the parameters
        parsedParameters = parameterParse(extraMerge, parameters)

        if (parsedParameters == None):
            print("\n !!! TASK NOT MODIFIED !!! \n")
            return
        for parameter in parsedParameters:
            if(parameter.getName() == 'tID'):
                # ASSURANCE
                taskList = self.database.getTaskByID(parameter.getValue())

                if(taskList == None):
                    print("\n !!! Cannot find task {taskName} !!! \n".format(
                        taskName=parameter.getValue()))
                    return

                print()
                for task in taskList:
                    print(task)

                print("\n Are you sure you want to delete? \n")

                answer = input("(y,n)>")

                if(answer in ('y', 'yes', 'ok')):
                    self.database.clearTaskByID(parameter.getValue())

            elif(parameter.getName() == 'tName'):

                # ASSURANCE
                taskList = self.database.getTasksNameFiltered(
                    parameter.getValue())
                if(taskList == None):
                    print("\n !!! Cannot find task {taskName} !!! \n".format(
                        taskName=parameter.getValue()))
                    return

                print()
                for task in taskList:
                    print(task)

                print("\n Are you sure you want to delete? \n")

                answer = input("(y,n)>")

                if(answer in ('y', 'yes', 'ok')):
                    self.database.clearTaskByName(parameter.getValue())

            else:
                print("\n !!! ERROR PARSED PARAMETERS - {parameterName}!!!".format(
                    parameterName=parameter.getName()))
    # -------- View tasks on database ------------
    # view all tasks

    def commandShowAll(self, extra=None):
        """
        Shows all the tasks on todo list

        Usage:
            todo show all

        """

        allTasks = self.database.getAllTasks()

        if(len(allTasks) == 0):
            print("\n ... Todo list empty ... \n")
            return

        self.printList(allTasks)

    def commandShowSort(self, extra=None):
        """
        Shows sorted database

        Usage: todo show sort [PARAMETER]

        e.g - todo show sort -p |asc/desc|

        Parameters:
            -p  -------- sort by parameter
            -n --------- sort by name

            OPTIONAL
            asc/desc ------ asc or desc


        """
        sortedTasks = []
        if(len(extra) == 0):
            # Defaulat sorted by priority
            # TODO optimize sorting system
            sortedTasks = self.database.getTasksPrioritySorted("asc")
        elif(len(extra) > 1):

            if(not (extra[1] == "asc" or extra[1] == "desc")):
                print(extra[1], "unknown")
                return

            if(extra[0] == '-p'):
                sortedTasks = self.database.getTasksPrioritySorted(extra[1])
            elif(extra[0] == '-n'):
                sortedTasks = self.database.getTasksNameSorted(extra[1])
            else:
                print("!!! Unknown Command !!!")
                return
        else:
            if(extra[0] == '-p'):
                sortedTasks = self.database.getTasksPrioritySorted()
            elif(extra[0] == '-n'):
                sortedTasks = self.database.getTasksNameSorted()
            else:
                print("!!! Unknown Command !!!")
                return

        if(len(sortedTasks) == 0):
            print("\n ... Todo list empty ... \n")

        self.printList(sortedTasks)

    def commandShow(self, extra=None):
        filteredTasks = []

        if(len(extra) == 0):
            print("!!! No parameters added !!!")
            return

        extraMerge = " ".join(extra)

        # TODO to be optimized later

        parameters = [
            Parameter(parameterName="tID", singleDash="i",
                      doubleDash="id", isRequired=False,
                      inputType="int"),

            Parameter(parameterName="tName", singleDash="n",
                      doubleDash="name", isRequired=False),

            Parameter(parameterName="tType", singleDash="t",
                      doubleDash="type", isRequired=False),

            Parameter(parameterName="tRepeat", singleDash="r",
                      doubleDash="repeat", isRequired=False,
                      inputType="bool"),

            Parameter(parameterName="tPriority", singleDash="p",
                      doubleDash="priority", isRequired=False)
        ]

        # ------  Custom Validation Functions ---------
        # Task Type Validation

        self.searchParameterList("tType", parameters).setCustomValidation(
            TodoHandler.taskTypeValidation
        )
        # Task Priority Validation

        self.searchParameterList("tPriority", parameters).setCustomValidation(
            TodoHandler.taskPriorityValidation
        )
        # ------------------------------------------------

        # Handle multi line input
        extraMerge = InputHandler.multilineInput(extraMerge, "todo show task")

        # parse the arguments for the parameters
        parsedParameters = parameterParse(extraMerge, parameters)

        if (parsedParameters == None):
            print("!!! Error  !!!")
            # Exception
            return

        # Get values
        for parameter in parsedParameters:
            if (parameter.getName() == "tName"):
                filteredTasks = self.database.getTasksNameFiltered(
                    parameter.getValue())
            elif (parameter.getName() == "tType"):
                filteredTasks = self.database.getTasksTypeFiltered(
                    parameter.getValue())
            elif (parameter.getName() == "tRepeat"):
                filteredTasks = self.database.getTasksRepeatFiltered(
                    parameter.getName())
            elif (parameter.getName() == "tPriority"):
                filteredTasks = self.database.getTasksPriorityFiltered(
                    parameter.getValue())
            elif (parameter.getName() == "tID"):
                filteredTasks = self.database.getTaskByID(
                    parameter.getValue())
            else:
                print("\n ... Parameter setup incorrect ... \n")
                return

        if(filteredTasks == None):
            # TODO Custom Exception
            return

        if(len(filteredTasks) == 0):
            print("\n ... No tasks fit parameter ... \n")
            return

        self.printList(filteredTasks)


if (__name__ == "__main__"):

    # input test
    todo = TodoHandler("db")
    s = "-n{test test} -p{test test}"
    todo.commandNewTask(s.split())
