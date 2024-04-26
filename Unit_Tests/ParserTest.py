import unittest
from Parser import Parser

class TestParse(unittest.TestCase):
    def test_var_assign(self):
       tokens =  [('NEWLINE', '\n'), ('INDENT', 12), ('IDENTIFIER', 'x'), ('EQUALS', '='), ('NUMBER', '5'), ('NEWLINE', '\n'),
         ('DEDENT', 12), ('NEWLINE', '\n')]

       expected_parsed = [('ASSIGNMENT', 'x', ('NUMBER', '5'))]

       P = Parser(tokens)
       parsed = P.parse()

       self.assertEqual(parsed, expected_parsed)


    def test_built_in_functions(self):
        tokens = [('NEWLINE', '\n'), ('INDENT', 12), ('PRINT', 'print'), ('PIPE', '|'), ('STRING', 'wow'), ('PIPE', '|'), ('NEWLINE', '\n'), ('DEDENT', 12), ('NEWLINE', '\n')]

        expected_parsed = [('PRINT', [('STRING', 'wow')])]

        P = Parser(tokens)
        parsed = P.parse()

        self.assertEqual(parsed, expected_parsed)

        tokens = [('INDENT', 1), ('NEWLINE', '\n'), ('INDENT', 13), ('IDENTIFIER', 'x'), ('EQUALS', '='), ('KINETIC_ENERGY', 'kinetic_energy'), ('PIPE', '|'), ('NUMBER', '2'), ('NUMBER', '4'), ('PIPE', '|'), ('NEWLINE', '\n'), ('DEDENT', 13), ('DEDENT', 9), ('INDENT', 8), ('NEWLINE', '\n')]

        expected_parsed = [('ASSIGNMENT', 'x', ('KINETIC_ENERGY', [('NUMBER', '2'), ('NUMBER', '4')]))]

        P = Parser(tokens)
        parsed = P.parse()

        self.assertEqual(parsed, expected_parsed)

    def test_if_statement(self):
        tokens = [('NEWLINE', '\n'), ('INDENT', 12), ('KEYWORD', 'if'), ('IDENTIFIER', 'x'), ('GREATER_THAN', '>'), ('NUMBER', '5'), ('COLON', ':'), ('NEWLINE', '\n'), ('INDENT', 16), ('PRINT', 'print'), ('PIPE', '|'), ('STRING', 'Hello, world!'), ('PIPE', '|'), ('NEWLINE', '\n'), ('NEWLINE', '\n'), ('DEDENT', 16), ('KEYWORD', 'else'), ('COLON', ':'), ('NEWLINE', '\n'), ('INDENT', 16), ('PRINT', 'print'), ('PIPE', '|'), ('STRING', 'Goodbye, world!'), ('PIPE', '|'), ('NEWLINE', '\n'), ('DEDENT', 16), ('DEDENT', 12), ('NEWLINE', '\n')]
        expected_parsed = [('IF_STATEMENT', ('GREATER_THAN', ('IDENTIFIER', 'x'), ('NUMBER', '5')), [[('PRINT', [('STRING', 'Hello, world!')])]], [[('PRINT', [('STRING', 'Goodbye, world!')])]])]

        P = Parser(tokens)
        parsed = P.parse()

        self.assertEqual(parsed, expected_parsed)

    def test_while_loop(self):
        tokens =  [('NEWLINE', '\n'), ('INDENT', 8), ('IDENTIFIER', 'count'), ('EQUALS', '='), ('NUMBER', '5'), ('NEWLINE', '\n'),
         ('KEYWORD', 'while'), ('IDENTIFIER', 'count'), ('GREATER_THAN', '>'), ('NUMBER', '0'), ('COLON', ':'),
         ('NEWLINE', '\n'), ('INDENT', 12), ('PRINT', 'print'), ('PIPE', '|'), ('STRING', 'Count:'),
         ('IDENTIFIER', 'count'), ('PIPE', '|'), ('NEWLINE', '\n'), ('IDENTIFIER', 'count'), ('EQUALS', '='),
         ('IDENTIFIER', 'count'), ('SUBTRACT', '-'), ('NUMBER', '1'), ('NEWLINE', '\n'), ('DEDENT', 12),
         ('NEWLINE', '\n')]

        expected_parsed = [('ASSIGNMENT', 'count', ('NUMBER', '5')), ('WHILE_LOOP', ('GREATER_THAN', ('IDENTIFIER', 'count'), ('NUMBER', '0')), [[('PRINT', [('STRING', 'Count:'), ('IDENTIFIER', 'count')]), ('ASSIGNMENT', 'count', ('SUBTRACT', ('IDENTIFIER', 'count'), ('NUMBER', '1')))]])]



        P = Parser(tokens)
        parsed = P.parse()

        #print(parsed)

        self.assertEqual(parsed, expected_parsed)