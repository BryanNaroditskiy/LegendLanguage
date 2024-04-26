import unittest
from Interpeter import Interpreter  # Import the lex function from your module

class TestInterp(unittest.TestCase):
    def test_var_assign(self):
        parser = [('ASSIGNMENT', 'x', ('NUMBER', '5'))]
        expected = "x = 5.0\n"
        I = Interpreter.interpret(parser)
        self.assertEqual(I, expected)
    def test_built_in_functions(self):
        parser = [('PRINT', [('STRING', 'wow')])]
        expected = "print('wow')\n"
        I = Interpreter.interpret(parser)
        self.assertEqual(I, expected)

        parser = [('ASSIGNMENT', 'x', ('KINETIC_ENERGY', [('NUMBER', '2'), ('NUMBER', '4')]))]
        expected = "x = 16.0\n"
        I = Interpreter.interpret(parser)
        self.assertEqual(I, expected)

    # def test_if_statements(self):
    #     parser = [('IF_STATEMENT', ('GREATER_THAN', ('IDENTIFIER', 'x'), ('NUMBER', '5')), [[('PRINT', [('STRING', 'Hello, world!')])]], [[('PRINT', [('STRING', 'Goodbye, world!')])]])]
    #     I = Interpreter.interpret(parser)
    #     print(I)
    #
    #     #self.assertEqual(I, expected)
    #
    # def test_while_loop(self):
    #     parser = [('ASSIGNMENT', 'count', ('NUMBER', '5')), ('WHILE_LOOP', ('GREATER_THAN', ('IDENTIFIER', 'count'), ('NUMBER', '0')), [[('PRINT', [('STRING', 'Count:'), ('IDENTIFIER', 'count')]), ('ASSIGNMENT', 'count', ('SUBTRACT', ('IDENTIFIER', 'count'), ('NUMBER', '1')))]])]
    #     I = Interpreter.interpret(parser)
    #     expected = """
    #     count = 5.0
    #     while count > 0.0:
    #         print('Count:', count)
    #         count = count - 1.0 """
    #     print(I)
    #     self.assertEqual(I, expected)

    # def test_if_statements(self):
    # def test_built_in_functions(self):
    # def test_while_loops(self):