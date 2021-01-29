import types


class IncorrectHandlerFormat(Exception):

    def __init__(self, path, message="Handler function has not been configured properly"):
        self.path = path
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return f"{self.path} -> {self.message}"


class Handler():
    """
    ---------------------------------------------------
    command format is
    command : {
        "default" : to run when there is no extra commands
        "help" : help text / description text
    }
    ALL functions/methods added should have a string array
    argument attached i.e Method(self, extra)/Function(extra)
    ---------------------------------------------------
    """

    def __init__(self):
        self.commands = {
            "default": None,
            "help": None
        }

    def getCommands(self):
        return self.commands

    def help(self, extra=None):
        print("\n ---- HELP ----\n")
        self.printBaseCommands(self.commands)
        while (True):
            print()
            print("-" * 30)
            print("when done type 'done' or 'exit' ")
            print("To show help text type 'help'")
            print("-" * 30)
            enter = input("HELP>")
            enter = enter.strip()
            print()

            # to leave the help section
            if(enter == 'done' or enter == 'exit'):
                break

            # if input is empty
            if(len(enter) == 0):
                continue

            # if there is one input string
            elif(len(enter.split()) == 1):
                if(enter == 'help'):
                    print("\n ---- HELP ----\n")
                    self.printBaseCommands(self.commands)
                    continue

                if(not enter in self.commands):
                    print("!!! {} Command Unknown !!!".format(enter))
                else:
                    if(isinstance(self.commands[enter], (types.MethodType))):
                        print(self.commands[enter].__doc__)
                    elif(isinstance(self.commands[enter], dict)):
                        if("default" in self.commands[enter]):
                            self.printDeepHelpText(
                                self.commands[enter]['default'], enter + " default")
                        print()
                        if("help" in self.commands[enter]):
                            self.printDeepHelpText(
                                self.commands[enter]['help'], enter + " help")

            # if there is more than one strings
            else:
                enterSplit = enter.split()
                dictionaries = self.commands
                for i in enterSplit:
                    if(not i in dictionaries):
                        print("!!! Cannot view help for {} !!!".format(i))
                        break
                    if(isinstance(dictionaries[i], dict)):
                        dictionaries = dictionaries[i]

                    elif(isinstance(dictionaries[i], (types.MethodType))):
                        print(dictionaries[i].__doc__)
                    elif(isinstance(dictionaries[i], str)):
                        print(dictionaries[i])
                    else:
                        print("!!! {} unknown help format !!!".format(i))
                        print("ERROR")
                        break

    def printDeepHelpText(self, helpObject, extra="help"):
        # print help function for dictionary tree nodes
        if(isinstance(helpObject, dict)):
            if("default" in helpObject):
                self.printDeepHelpText(
                    helpObject["default"], extra + " " + "default")

        elif(isinstance(helpObject, str)):
            print(helpObject)
        elif(isinstance(helpObject, (types.MethodType))):
            print(helpObject.__doc__)
        elif(helpObject == None):
            print("{} is unavailable".format(extra))
        else:
            print("{} is unknown help format".format(extra))

    def printBaseCommands(self, dictionary, extra=""):
        # To list out all the dictionary tree nodes
        for i in dictionary:
            if(i == "default" or i == "help"):
                continue
            print(" -" + extra + i)
            if(isinstance(dictionary[i], dict)):
                self.printBaseCommands(dictionary[i], extra + i + " ")


class InputHandler(Handler):
    def __init__(self):

        self.isExit = False
        self.defaultValues = ["help", "default"]
        self.commands = {

            # default commands
            "help": {
                "default": self.helpManager,
                "help": "Displays help text - to see more detailed help type help more",
                "more": self.help
            },

            "exit": {
                "default": self.exitManager,
                "help": "Closes application"

            }
        }

    def handle(self, inputText):

        commandSplit = inputText.split()

        # if the input line is empty
        if (len(commandSplit) < 1):
            print("Empty input")
            return

        # if the first string is not in the command dictionary
        if (not commandSplit[0].lower() in self.commands):
            print("Command not recognized")
            return

        # if there is only one string run default
        if (len(commandSplit) < 2):
            # if default is not empty
            self.defaultInput(
                commandSplit, self.commands[commandSplit[0].lower()])
        else:
            self.multiInput(
                commandSplit, self.commands[commandSplit[0].lower()])

    # TODO refactor and optimize "commandSplit and command? really?"
    def defaultInput(self, commandSplit, command):

        if (command["default"] == None):
            self.printHelp(command['help'])
        elif (isinstance(command["default"], (types.FunctionType, types.MethodType))):
            # if method/function, run with extra inputs as arguments
            command["default"](commandSplit)
        elif (isinstance(command["default"], str)):
            # if string print the string
            print(command["default"])
        else:
            print("Error: unsupported default data type " + type(command))

    def multiInput(self, commandSplit, command):

        for i in range(1, len(commandSplit)):
            # if the input text is not in command dictionary
            if (not commandSplit[i].lower() in command):
                self.printHelp(command['help'])
                break

            value = command[commandSplit[i].lower()]

            if (isinstance(value, dict)):

                # if dictionary, set command to value
                command = value

                if (i + 1 == len(commandSplit)):
                    # if there are no more parameters
                    self.defaultInput(commandSplit[(i+1):], command)
                else:
                    # TODO How to tell the difference between parameters and commands
                    if(commandSplit[i+1][0] == "-"):
                        self.defaultInput(commandSplit[(i+1):], command)
                        break

            elif (isinstance(value, (types.FunctionType, types.MethodType))):
                # if method/function, run with extra inputs as arguments

                if (commandSplit[-1] == "help"):
                    self.printHelp(command['help'])
                    break
                value(commandSplit[(i + 1)::])
                break
            elif (isinstance(value, str)):
                # if string print the string
                print(value)
                break
            elif (value == None):
                # if value is None
                # print a error
                print("None")
                break
            else:
                print("Error: unsupported data type")
                break

    def addHandler(self, handlerName, handler):
        # Check handler configuration
        self.configCheck(handler.getCommands(), handlerName)

        # inserts handler into command dictionary
        self.commands[handlerName] = handler.getCommands()

    def configCheck(self, commands, name):
        # Check if handler command has default values
        for i in self.defaultValues:
            if (not i in commands):
                # if default values not assigned print warning
                print("* {} is not in command {}".format(i, name))
                commands[i] = None

        # Go throught the command dictionary
        for key in commands:
            if (isinstance(commands[key], dict)):
                # if type dictionary, recurse with dictionary
                self.configCheck(commands[key], name + " > " + key)
            elif (isinstance((commands[key]), (types.FunctionType, types.MethodType))):
                # if type method, check if its format Function(extra)
                numArguments = commands[key].__code__.co_argcount
                if (numArguments != 2):
                    raise IncorrectHandlerFormat(
                        name + " > " + commands[key].__code__.co_name + "(self)")

    @staticmethod
    def multilineInput(lineInput, prompt="continue"):

        if (isinstance(lineInput, str)):
            inputList = lineInput.split()
        elif (isinstance(lineInput, list)):
            inputList = lineInput
        else:
            raise TypeError("Multiline Input should be list or string")

        # multiline input for parameters
        if (inputList[0] == "("):
            done = False
            newlineParameters = inputList[-1]
            while (not done):
                if (newlineParameters[-1] == ")"):
                    inputList += newlineParameters[:-1]
                    done = True
                else:
                    newlineParameters = input(prompt + ">")
                    newlineParameters = newlineParameters.strip()
                    inputList += newlineParameters

        return " ".join(inputList)

    def printHelp(self, helpCommand):
        # Prints help for deeper functions if there is a input error
        # todo newtask
        if (isinstance(helpCommand, (types.FunctionType, types.MethodType))):
            print(helpCommand())
        elif (isinstance(helpCommand, str)):
            print(helpCommand)
        elif (isinstance(helpCommand, dict)):
            print(helpCommand["help"])
        elif (helpCommand == None):
            print("Help not available")
        else:
            print("Help command has unsupported data type")

    def helpManager(self, extra=None):
        # Specific help for base commands
        # ie >help

        print()
        # Iterate through commands and finds help text
        for command in self.commands:
            helpCommand = self.commands[command]['help']
            if (isinstance(helpCommand, (types.FunctionType, types.MethodType))):
                print(command + " - " + helpCommand(extra))
            elif (isinstance(helpCommand, str)):
                print(command + " - " + helpCommand)
            elif (isinstance(helpCommand, dict)):
                if (helpCommand["default"] == None):
                    print(command + " - " + "help is not available")
                else:
                    print(command + " - " + helpCommand["default"])
        print()

    def exitManager(self, extra=""):

        # close database and stuff
        print(" GOODBYE .... ^-^ ")
        self.isExit = True
