
class Parameter:
    def __init__(self, parameterName, singleDash, doubleDash, isRequired=False, inputType="str"):
        # static attributes
        self.parameterName = parameterName
        self.singleDash = singleDash
        self.doubleDash = doubleDash
        self.isRequired = isRequired
        self.inputType = inputType

        # attributes
        self.value = None
        self.validationFunction = self.getValidFunction()

    def setVal(self, value):
        value = self.validationFunction(value)

        if (value == None):
            return

        self.value = value

    def getName(self):
        return self.parameterName

    def getValue(self):
        return self.value

    def getValidFunction(self):

        if (self.inputType == "str"):
            return validateString
        elif (self.inputType == "int"):
            return validateInt
        elif (self.inputType == "bool"):
            return validateBool
        else:
            return

    def setCustomValidation(self, validationFunction):
        self.validationFunction = validationFunction

    def __str__(self):
        return self.parameterName


def validateString(value):
    return value


def validateInt(value):
    if (not value.isnumeric()):
        print("!!! {} not a valid integer input !!!".format(value))
        return
    intValue = int(value)
    return intValue


def validateBool(value):
    positive = ['yes', 'y', 'true', 'ok', 'yeah', 't']
    negative = ['no', 'n', 'false', 'nah', 'f']

    boolValue = None
    if (value.lower() in positive):
        boolValue = True
    elif (value.lower() in negative):
        boolValue = False
    else:
        print("!!! {} not valid boolean input !!!".format(value))

    return boolValue


def checkRequiredParameters(allParameters, parametersWithValues):
    # Check if required parameters are set
    # Prompt if they are not set
    for parameter in allParameters:
        if (parameter.isRequired):
            if (not parameter in parametersWithValues):
                noTextInput = input(
                    "Enter " + parameter.parameterName + ":")
                parameter.setVal(noTextInput)
                parametersWithValues.append(parameter)

    return parametersWithValues


def parameterParse(arguments, parameters):

    State = {
        "Out": 0,
        "In": 1,
        "Dash": 2,
        "DoubleDash": 3
    }

    currentState = State["Out"]
    currentParameter = None
    returnParameters = []
    parameterText = ""
    doubleDashText = ""

    for i in arguments:

        # IF i IS NOT ON PARAMETER
        if (currentState == State["Out"]):
            if (i == "-"):
                currentState = State["Dash"]

        # IF i IS AFTER A DASH
        elif (currentState == State["Dash"]):
            if (i == "-"):
                currentState = State["DoubleDash"]
            elif (i == "{"):
                if (currentParameter == None):
                    print("Error: " + i + " No parameters added")
                    return
                else:
                    parameterText = ""
                    currentState = State["In"]
            elif (i == "}"):
                print("Error: " + i + " incorrect syntax")
                return
            else:
                for parameter in parameters:
                    # Check if there are more than one single dash characters
                    if (currentParameter != None):
                        print("Too many parameters -" + currentParameter.singleDash +
                              " not -" + currentParameter.singleDash + i.lower())
                        return

                    if ((i.lower()) == parameter.singleDash):
                        currentParameter = parameter
                        break
                if (currentParameter == None):
                    print("Error -" + i + " is not a valid parameter")
                    return
        # IF i AFTER DOUBLE DASH
        elif (currentState == State["DoubleDash"]):
            if(i == "-"):
                print("!!! Too many dashes !!!")
                return
            elif(i == "{"):
                if(doubleDashText == ""):
                    print("Error:" + i + "No paramters added")
                    return
                for parameter in parameters:
                    if(currentParameter != None):
                        print(
                            "Error: too many parameters  - {}".format(doubleDashText))
                        return

                    if(doubleDashText == parameter.doubleDash):
                        currentParameter = parameter
                        break
                if(currentParameter == None):
                    print("Error - " + doubleDashText +
                          " is not a valid parameter")
                    return

                parameterText = ""
                doubleDashText = ""
                currentState = State["In"]
            elif(i == "}"):
                print("Error: " + i + " incorrect syntax")
                return
            else:
                doubleDashText += i.lower()

        # IF i IS IN PARAMETER TEXT
        elif (currentState == State["In"]):
            # set value to parameter
            # change state to outside parameter
            if (i == "}"):
                currentParameter.setVal(parameterText)
                returnParameters.append(currentParameter)
                currentParameter = None
                currentState = State["Out"]
            else:
                parameterText = parameterText + i
    return returnParameters
