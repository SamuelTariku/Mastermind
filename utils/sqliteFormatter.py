
import types

# Format the data object


def sqliteFormat(obj):
    if(isinstance(obj, str)):
        newString = "'" + obj + "'"
        return newString
    elif(isinstance(obj, bool)):
        if(obj):
            return str(1)
        else:
            return str(0)
    elif(isinstance(obj, int)):
        return str(obj)
    elif(obj == None):
        return 'NULL'


# Includes the comparisors
def sqliteBeginsWithFormat(string):
    return "like '%" + string + "'"


def sqliteEndsWithFormat(string):
    return "like '" + string + "%'"


def sqliteContainsFormat(string):
    return "like '%" + string + "%'"


if __name__ == "__main__":
    print(sqliteFormat(True))
