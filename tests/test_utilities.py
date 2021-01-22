import unittest
from utils.utilities import *


class utilitiesTests(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)

        # Test parameters used to check what works
        self.parameters = [
            Parameter("tName", "n", "name", True, "str"),
            Parameter("tType", "t", "type", True, "str"),
            Parameter("tRepeat", "r", "repeat", True, "bool"),
            Parameter("tPriority", "p", "priority", False, "str")
        ]

    def test_parameters_size(self):
        # check how many parameters are returned

        arguments = "-n{work on todo list} -t{normal} -p{INU}"
        result = parameterParse(arguments, self.parameters)
        self.assertEqual(len(result), 3)

    def test_valid_parameters(self):
        # check if the correct parameters are returned

        arguments = "-n{work on todo list}"
        result = parameterParse(arguments, self.parameters)

        if (len(result) > 0):
            self.assertEqual(result[0].getName(), "tName")
        else:
            assert False, "Function returns empty"

    def test_correct_parameter_value(self):
        # check if the correct parameters are returned

        arguments = "-n{work on todo list}"
        result = parameterParse(arguments, self.parameters)

        if (len(result) > 0):
            self.assertEqual(result[0].getValue(), "work on todo list")
        else:
            assert False, "Function returns empty"

    def test_double_dash(self):
        arguments = "--name{work on todo list} --type{normal} --priority{INU}"
        result = parameterParse(arguments, self.parameters)
        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()
