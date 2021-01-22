
class Task():

    # So that all the changes can be controlled
    # from one area

    configParameters = {
        "required": {
            # table field names
            "fields": ['name', 'type', 'repeat'],

            # Attribute name
            "attributes": ['taskName', 'taskType', 'taskRepeat']
        },

        "optional": {
            # table field names
            "fields": ['priority'],

            # Attribute name
            "attributes": ['taskPriority']
        },

        "id": {
            "field": 'id',
            "attribute": 'taskID'
        },
    }

    prioritySetUp = ['iu', 'inu', 'niu', 'ninu']

    def __init__(self, taskName, taskType, taskRepeat):

        self.taskID = None

        # Required parameters
        self.taskName = taskName
        self.taskType = taskType
        self.taskRepeat = taskRepeat

        # Optional parameters
        self.taskPriority = None

    # Task id is autoincremented by database
    def setID(self, taskID):
        self.taskID = taskID

    def addPriority(self, priority):
        self.taskPriority = priority
        pass

    def getPriority(self):
        return self.taskPriority

    @staticmethod
    def getConfig(isRequired=False, parameter=None):
        requiredState = "optional"
        if(isRequired):
            requiredState = "required"

        if(parameter == None):
            print("No parameters entered")
            return

        if(not parameter in ('fields', 'attributes')):
            print("Incorrect parameter type")
            return

        return Task.configParameters[requiredState][parameter]

    @staticmethod
    def getConfigID(parameter=None):
        if(parameter == None):
            print("No parameters entered")
            return
        return Task.configParameters['id'][parameter]

    def __str__(self):
        taskString = []

        if(self.taskID != None):
            taskString.append(str(self.taskID))
        else:
            taskString.append("-")

        if(self.taskName != None):
            taskString.append(self.taskName)
        else:
            taskString.append("-")

        if(self.taskType != None):
            taskString.append(self.taskType)
        else:
            taskString.append("-")

        if(self.taskRepeat != None):
            taskString.append(str(self.taskRepeat))
        else:
            taskString.append("-")

        if(self.taskPriority != None):
            taskString.append(self.taskPriority)
        else:
            taskString.append("-")

        return " | ".join(taskString)


class ModTask():
    def __init__(self):

        self.taskID = None

        self.taskName = None
        self.taskType = None
        self.taskRepeat = None

        self.taskPriority = None

    # -------GETTERS-------
    def getTaskID(self):
        return self.taskID

    def getTaskName(self):
        return self.taskName

    def getTaskType(self):
        return self.taskType

    def getTaskRepeat(self):
        return self.taskRepeat

    def getTaskPriority(self):
        return self.getTaskPriority

    # ---------SETTERS---------
    def setTaskID(self, taskID):
        self.taskID = taskID

    def setTaskName(self, taskName):
        self.taskName = taskName

    def setTaskType(self, taskType):
        self.taskType = taskType

    def setTaskRepeat(self, taskRepeat):
        self.taskRepeat = taskRepeat

    def setTaskPriority(self, taskPriority):
        self.taskPriority = taskPriority


class TaskBuilder():
    @staticmethod
    def build(taskName, taskType, taskRepeat, taskPriority=None, taskID=None):

        taskName = TaskBuilder.checkType(taskName, str)
        taskType = TaskBuilder.checkType(taskType, str)
        taskRepeat = TaskBuilder.checkType(taskRepeat, bool)

        newTask = Task(taskName, taskType, taskRepeat)
        if(taskID != None):
            taskID = TaskBuilder.checkType(taskID, int)
            newTask.setID(taskID)
        if(taskPriority != None):
            taskPriority = TaskBuilder.checkType(taskPriority, str)
            newTask.addPriority(taskPriority)

        return newTask

    @staticmethod
    def buildMod(taskName=None, taskType=None, taskRepeat=None, taskPriority=None, taskID=None):

        newModTask = ModTask()
        newModTask.setTaskID(taskID)
        newModTask.setTaskName(taskName)
        newModTask.setTaskType(taskType)
        newModTask.setTaskRepeat(taskRepeat)
        newModTask.setTaskPriority(taskPriority)

        return newModTask

    @staticmethod
    def checkType(obj, sType):
        returnObj = None
        try:
            returnObj = sType(obj)
        except TypeError as e:
            print("TaskBuilder: Cannot create task")
            print(e)

        return returnObj
