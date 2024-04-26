import unittest
from LexicalAnalyzer import lex  # Import the lex function from your module

class TestLex(unittest.TestCase):

    def test_var_assign(self):
        code = """
            x = 5
        """

        expected_tokens = [('NEWLINE', '\n'), ('INDENT', 12), ('IDENTIFIER', 'x'), ('EQUALS', '='), ('NUMBER', '5'), ('NEWLINE', '\n'), ('DEDENT', 12), ('NEWLINE', '\n')]
        print(lex(code))
        self.assertEqual(lex(code), expected_tokens)

    def test_if_statements(self):
        code = """
            if x > 5:
                print("Hello, world!")
            else:
                print("Goodbye, world!")
        """
        expected_tokens = [('NEWLINE', '\n'), ('INDENT', 12), ('KEYWORD', 'if'), ('IDENTIFIER', 'x'), ('GREATER_THAN', '>'), ('NUMBER', '5'), ('COLON', ':'), ('NEWLINE', '\n'), ('INDENT', 16), ('PRINT', 'print'), ('LEFT_PAREN', '('), ('STRING', 'Hello, world!'), ('RIGHT_PAREN', ')'), ('NEWLINE', '\n'), ('DEDENT', 16), ('KEYWORD', 'else'), ('COLON', ':'), ('NEWLINE', '\n'), ('INDENT', 16), ('PRINT', 'print'), ('LEFT_PAREN', '('), ('STRING', 'Goodbye, world!'), ('RIGHT_PAREN', ')'), ('NEWLINE', '\n'), ('DEDENT', 16), ('DEDENT', 12), ('NEWLINE', '\n')]

        self.assertEqual(lex(code), expected_tokens)

    def test_built_in_function(self):
        code = """
            print|"wow"|
        """

        expected_tokens = [('NEWLINE', '\n'), ('INDENT', 12), ('PRINT', 'print'), ('PIPE', '|'), ('STRING', 'wow'), ('PIPE', '|'), ('NEWLINE', '\n'), ('DEDENT', 12), ('NEWLINE', '\n')]

        self.assertEqual(lex(code), expected_tokens)

        code = """
            sin|45|
        """

        expected_tokens = [('NEWLINE', '\n'), ('INDENT', 12), ('SIN', 'sin'), ('PIPE', '|'), ('NUMBER', '45'), ('PIPE', '|'), ('NEWLINE', '\n'), ('DEDENT', 12), ('NEWLINE', '\n')]

        self.assertEqual(lex(code), expected_tokens)

        code = """ 
             kinetic_energy | 2, 4 |
        """
        expected_tokens = [('INDENT', 1), ('NEWLINE', '\n'), ('INDENT', 13), ('KINETIC_ENERGY', 'kinetic_energy'), ('PIPE', '|'), ('NUMBER', '2'), ('NUMBER', '4'), ('PIPE', '|'), ('NEWLINE', '\n'), ('DEDENT', 13), ('DEDENT', 9), ('INDENT', 8), ('NEWLINE', '\n')]
        self.assertEqual(lex(code), expected_tokens)

    def test_while_loop(self):
        code = """
        count = 5
        while count > 0:
            print|"Count:", count|
            count = count - 1
        """

        expected_tokens =  [('NEWLINE', '\n'), ('INDENT', 8), ('IDENTIFIER', 'count'), ('EQUALS', '='), ('NUMBER', '5'), ('NEWLINE', '\n'),
         ('KEYWORD', 'while'), ('IDENTIFIER', 'count'), ('GREATER_THAN', '>'), ('NUMBER', '0'), ('COLON', ':'),
         ('NEWLINE', '\n'), ('INDENT', 12), ('PRINT', 'print'), ('PIPE', '|'), ('STRING', 'Count:'),
         ('IDENTIFIER', 'count'), ('PIPE', '|'), ('NEWLINE', '\n'), ('IDENTIFIER', 'count'), ('EQUALS', '='),
         ('IDENTIFIER', 'count'), ('SUBTRACT', '-'), ('NUMBER', '1'), ('NEWLINE', '\n'), ('DEDENT', 12),
         ('NEWLINE', '\n')]
        self.assertEqual(lex(code), expected_tokens)





if __name__ == '__main__':
    unittest.main()
