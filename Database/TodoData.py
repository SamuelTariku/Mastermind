from Database.DAL import *
from Models.Task import *
from utils.sqliteFormatter import *
import sqlite3


class TodoData(DAL):

    def __init__(self, database, table):
        super().__init__(database, table)

        # check if table exists
        isDatabase = self.runDatabaseTest()

        isTable = True

        if(isDatabase):
            print("\n ... connected to database {databaseName} ... \n".format(
                databaseName=self.database.split("\\")[-1]))
            isTable = self.runTableTest()
        else:
            # sqlite creates database if it cants find a database
            return

        if(not isTable):
            createStatement = """
                CREATE TABLE Todo (
	            "ID"	INTEGER NOT NULL UNIQUE,
	            "Name"	TEXT NOT NULL,
	            "Type"	TEXT NOT NULL,
	            "Repeat"	INTEGER NOT NULL,
	            "Priority"	TEXT,
	            PRIMARY KEY("ID" AUTOINCREMENT)
                )
            """
            try:
                print("\n ...Creating Table... \n")
                self.conn.execute(createStatement)
            except Exception as e:
                print("ERROR cannot create table")
                print(e)
            print("\n  TABLE CREATED \n")

        self.taskIDField = Task.getConfigID('field')

        # Required fields
        self.requiredFields = Task.getConfig(
            isRequired=True, parameter='fields')

        # Model task attribute names to required fields
        self.requiredTaskAttributes = Task.getConfig(
            isRequired=True, parameter='attributes')

        # Optional fields
        self.optionalFields = Task.getConfig(
            isRequired=False, parameter='fields')

        # Model task attribute names to optional fields
        self.optionalTaskAttributes = Task.getConfig(
            isRequired=False, parameter='attributes')

        self.todoTableFields = ['id'] + \
            self.requiredFields + self.optionalFields
    # ------ Create ---------
    # Enter data into database

    def insertData(self, task):

        statement = "insert into {tableName}".format(
            tableName=self.table)

        fields = []
        values = []

        # Required Parameters
        for field in self.requiredFields:
            fields.append(field)

        for attribute in self.requiredTaskAttributes:
            values.append(sqliteFormat(
                getAttributeByString(Task, task, attribute)))

        # Optional Parameters
        # Check if assigned
        for attribute in self.optionalTaskAttributes:

            # Get value stored on task attribute using a string attribute name
            value = getAttributeByString(Task, task, attribute)

            if(value == None):
                continue

            fields.append(self.optionalFields[
                self.optionalTaskAttributes.index(attribute)
            ])

            values.append(sqliteFormat(value))

        strFields = ",".join(fields)
        strValues = ",".join(values)

        # structure the statement
        statement = "{statement} ({fields}) values ({values})".format(
            statement=statement, fields=strFields, values=strValues
        )

        try:
            self.conn.execute(statement)
            self.conn.commit()
        except Exception as e:
            print(e)
            print("\n ... Task not created .... \n")
            return

        print("\n ...Task added to database... \n")

    # ------------- Read ------------------
    # Get all tasks

    def getAllTasks(self):

        tasks = []

        statement = "select {fields} from {tableName} limit 0, 1000".format(
            fields=",".join(self.todoTableFields), tableName=self.table)

        try:
            cursor = self.conn.execute(statement)
        except Exception as e:
            print("/n ... Cannot retrieve tasks ... /n")
            return

        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

        return tasks

    # Get tasks by parameter
    def getTaskByID(self, id):
        tasks = []

        statement = "select {fields} from {tableName}".format(
            fields=",".join(self.todoTableFields), tableName=self.table)

        condition = "where {idField} = {idValue}".format(
            idField="id", idValue=id)

        try:
            cursor = self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
        except Exception as e:
            print("\n ... Cannot retrieve tasks ... \n")
            return

        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

        return tasks

    def getTasksPriorityFiltered(self, filter):

        tasks = []
        statement = "select {fields} from {tableName}".format(
            fields=",".join(self.todoTableFields), tableName=self.table)

        condition = "where {priorityField} = {priorityValue}"

        if(filter == 'iu'):
            condition = condition.format(
                priorityField='priority',
                priorityValue=sqliteFormat('iu')
            )
        elif(filter == 'inu'):
            condition = condition.format(
                priorityField='priority',
                priorityValue=sqliteFormat('inu')
            )
        elif(filter == 'niu'):
            condition = condition.format(
                priorityField='priority',
                priorityValue=sqliteFormat('niu')
            )
        elif(filter == 'ninu'):
            condition = condition.format(
                priorityField='priority',
                priorityValue=sqliteFormat('ninu')
            )
        else:
            print("\n ... Type not supported ... \n")
            return

        try:
            cursor = self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
        except Exception as e:
            print("/n ... Cannot retrieve tasks ... /n")
            print(e)
            return
        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

        return tasks

    def getTasksNameFiltered(self, filter):

        if(filter == None):
            print("\n !!! Filter Incorrect !!! \n")
            return

        tasks = []

        statement = "select {fields} from {tableName}".format(
            fields=",".join(self.todoTableFields), tableName=self.table)

        condition = "where {nameField} {nameValue}".format(
            nameField='name', nameValue=sqliteContainsFormat(filter))

        try:
            cursor = self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
        except Exception as e:
            print("/n ... Cannot retrieve tasks ... /n")
            print(e)
            return

        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

        return tasks

    def getTasksTypeFiltered(self, filter):

        tasks = []
        statement = "select {fields} from {tableName}".format(
            fields=",".join(self.todoTableFields), tableName=self.table)
        if(filter == 'normal'):
            condition = "where {typeField} {typeValue}".format(
                typeField='type', typeValue=sqliteContainsFormat('normal'))
        elif(filter == 'general'):
            condition = "where {typeField} {typeValue}".format(
                typeField='type', typeValue=sqliteContainsFormat('general'))
        else:
            print("\n ... Type not supported ... \n")
            return

        try:
            cursor = self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
        except Exception as e:
            print("/n ... Cannot retrieve tasks ... /n")
            print(e)
            return
        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

        return tasks

    def getTasksRepeatFiltered(self, filter):

        tasks = []

        statement = "select {fields} from {tableName}".format(
            fields=",".join(self.todoTableFields), tableName=self.table)
        if(filter == True):
            condition = "where {repeatField} = {repeatValue}".format(
                typeField='type', type=sqliteFormat(True))
        elif(filter == False):
            condition = "where {typeField} {typeValue}".format(
                typeField='type', type=sqliteFormat(False))
        else:
            print("\n ... Type not supported ... \n")
            return

        try:
            cursor = self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
        except Exception as e:
            print("/n ... Cannot retrieve tasks ... /n")
            print(e)
            return
        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

    # Get tasks sorted by parameter
    def getTasksPrioritySorted(self, direction="asc"):
        # FIXME
        tasks = self.getAllTasks()
        iu = []
        inu = []
        niu = []
        ninu = []
        notSorted = []

        sortedTasks = []

        for task in tasks:
            if(task.getPriority() == 'iu'):
                iu.append(task)

            elif(task.getPriority() == 'inu'):
                inu.append(task)

            elif(task.getPriority() == 'niu'):
                niu.append(task)

            elif(task.getPriority() == 'ninu'):
                ninu.append(task)

            elif(task.getPriority() == None):
                notSorted.append(task)

        if(direction == "asc"):
            sortedTasks = iu + inu + niu + ninu + notSorted
        elif(direction == "desc"):
            sortedTasks = ninu + niu + inu + iu + notSorted
        else:
            print(direction, "unknown")

        return sortedTasks

    def getTasksNameSorted(self, direction="asc"):
        tasks = []
        orderDirection = None

        if(not (direction == "asc" or direction == "desc")):
            print(direction, "Not Supported")

        statement = "select {fields} from {tableName}".format(
            fields=",".join(self.todoTableFields),
            tableName=self.table)

        condition = "order by {orderField} {direction}".format(
            orderField="name",
            direction=direction)

        print(statement)
        try:
            cursor = self.conn.execute(
                "{statement} {condition}  limit 0, 1000".format(
                    statement=statement,
                    condition=condition)
            )
        except Exception as e:
            print("/n ... Cannot retrieve tasks ... /n")
            print(e)
            return

        for row in cursor:
            task = TaskBuilder.build(
                taskID=row[self.todoTableFields.index("id")],
                taskName=row[self.todoTableFields.index("name")],
                taskType=row[self.todoTableFields.index("type")],
                taskRepeat=row[self.todoTableFields.index("repeat")],
                taskPriority=row[self.todoTableFields.index("priority")]
            )
            tasks.append(task)

        return tasks

    # --------------- Update -------------
    # update a task by finding id

    def updateByID(self, taskID, task):

        statement = "update {tableName}".format(tableName=self.table)

        fields = []
        values = []

        modFields = self.requiredFields + self.optionalFields
        modAttribute = self.requiredTaskAttributes + self.optionalTaskAttributes

        for attribute in modAttribute:
            if(attribute == None):
                continue

            # Get value stored on task attribute using a string attribute name
            value = getAttributeByString(Task, task, attribute)

            if(value == None):
                continue

            # Get the index of the attribute stored at modAttributes
            # use the index to get the fields stored at modFields
            fields.append(modFields[modAttribute.index(attribute)])

            values.append(sqliteFormat(value))

        strFields = ",".join(fields)
        strValues = ",".join(values)

        # set up statement
        statement = "{statement} set ({fields}) = ({values}) where {idfield} = {idValue}".format(
            statement=statement,
            fields=strFields,
            values=strValues,
            idfield=self.taskIDField,
            idValue=taskID
        )

        try:
            self.conn.execute(statement)
            self.conn.commit()
        except Exception as e:
            print(e)
            print("\n ... Task not updated ... \n")
            return

        print("\n ... Task has been updated ... \n")

    # ------------ Delete -----------
    # Clears all tasks in database
    def clearAllTasks(self):

        try:
            self.conn.execute("delete from {tableName}".format(
                tableName=self.table))
            self.conn.commit()
        except Exception as e:
            print(e)
            print("\n ... Database not cleared ... \n")
            return

        print("\n ... Database cleared ... \n")

    def clearTaskByID(self, id):
        statement = "delete from {tableName}".format(tableName=self.table)

        condition = "where {idField} = {idValue}".format(
            idField='id', idValue=sqliteFormat(id))

        # run statement
        try:
            self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
            self.conn.commit()

        except Exception as e:
            print("\n ... Task couldn't be deleted .. \n")
            return

        print("\n ... Task is deleted ... \n")

    def clearTaskByName(self, name):
        statement = "delete from {tableName}".format(tableName=self.table)

        condition = "where {nameField} {nameValue}".format(
            nameField='name', nameValue=sqliteContainsFormat(name))

        # run statement
        try:
            self.conn.execute("{statement} {condition}".format(
                statement=statement, condition=condition))
            self.conn.commit()

        except Exception as e:
            print("\n ... Task couldn't be deleted .. \n")
            return

        print("\n ... Task is deleted ... \n")


def getAttributeByString(atclass, atobj, string):

    # Takes the attribute name as a string and
    # gets the attribute stored on the object

    variable = atclass.__getattribute__(atobj, string)
    return variable
