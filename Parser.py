import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0

    def parse(self):
        print("Lexed")
        print("Starting parser...")
        statements = []
        while self.current_token_idx < len(self.tokens):
            print("Current token:", self.tokens[self.current_token_idx])
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        print("Parsed")
        return statements

    def parse_statement(self):
        token_type, token_value = self.peek()
        print("Current token in parse_statement:", token_type, token_value)
        if token_type == 'KEYWORD':
            if token_value == 'print':
                return self.parse_print_statement()
            elif token_value == 'if':
                return self.parse_if_statement()
            elif token_value == 'repeat':
                return self.parse_repeat_statement()
            else:
                # Handle other keyword statements
                pass
        elif token_type == 'IDENTIFIER':
            return self.parse_assignment_statement()
        elif token_type == 'COMMENT':
            self.advance()  # Consume comment tokens
            return None
        else:
            self.error("Unexpected token")

    def parse_print_statement(self):
        self.consume('KEYWORD', 'print')
        values = []
        while self.peek()[0] not in {'COMMENT', 'EOF'}:
            token_type, token_value = self.peek()
            if token_type in {'STRING', 'NUMBER', 'IDENTIFIER'}:
                values.append(token_value)
            elif token_type == 'OPERATOR' and token_value == ',':
                self.advance()  # Consume comma
            else:
                self.error("Unexpected token in print statement")
        return ('PRINT', values)

    def parse_if_statement(self):
        self.consume('KEYWORD', 'if')
        condition = self.parse_expression()
        block = self.parse_block()
        return ('IF', condition, block)

    def parse_repeat_statement(self):
        self.consume('KEYWORD', 'repeat')
        times = self.parse_expression()
        block = self.parse_block()
        return ('REPEAT', times, block)

    def parse_assignment_statement(self):
        identifier = self.consume('IDENTIFIER')[1]
        self.consume('OPERATOR', '=')
        value = self.parse_expression()
        return ('ASSIGN', identifier, value)

    def parse_expression(self):
        # Placeholder for parsing expressions
        # For now, assume simple arithmetic expressions
        expr = []
        while self.current_token_idx < len(self.tokens) and self.peek()[0] not in {'COMMENT', 'EOF', ';'}:
            token_type, token_value = self.peek()
            if token_type in {'NUMBER', 'IDENTIFIER', 'STRING'}:
                expr.append(token_value)
            elif token_type == 'OPERATOR':
                expr.append(token_value)
            self.advance()
        return ' '.join(expr)

    def parse_block(self):
        block = []
        self.consume('OPERATOR', '{')
        while self.peek()[1] != '}':
            statement = self.parse_statement()
            if statement:
                block.append(statement)
        self.consume('OPERATOR', '}')
        return block

    def consume(self, expected_type, expected_value=None):
        token_type, token_value = self.tokens[self.current_token_idx]
        if token_type != expected_type or (expected_value is not None and token_value != expected_value):
            self.error(
                f"Expected {expected_type}{' with value ' + expected_value if expected_value else ''}, got {token_type}{' with value ' + token_value if token_value else ''}")
        self.current_token_idx += 1
        return token_type, token_value

    def peek(self, offset=0):
        index = self.current_token_idx + offset
        if 0 <= index < len(self.tokens):
            return self.tokens[index]
        else:
            return 'EOF', None

    def advance(self):
        self.current_token_idx += 1

    def error(self, message):
        raise SyntaxError(message)




tokens = [('IDENTIFIER', 'speed'), ('OPERATOR', '='), ('NUMBER', '10'), ('NUMBER', '5'), ('IDENTIFIER', 'distance'), ('OPERATOR', '='), ('NUMBER', '100'), ('KEYWORD', 'time'), ('OPERATOR', '='), ('NUMBER', '2'), ('NUMBER', '5'), ('IDENTIFIER', 'mass'), ('OPERATOR', '='), ('NUMBER', '5'), ('IDENTIFIER', 'message'), ('OPERATOR', '='), ('STRING', 'Hello, Legend!'), ('IDENTIFIER', 'result1'), ('OPERATOR', '='), ('IDENTIFIER', 'distance'), ('OPERATOR', '/'), ('KEYWORD', 'time'), ('IDENTIFIER', 'result2'), ('OPERATOR', '='), ('IDENTIFIER', 'speed'), ('OPERATOR', '*'), ('KEYWORD', 'time'), ('IDENTIFIER', 'result3'), ('OPERATOR', '='), ('IDENTIFIER', 'mass'), ('OPERATOR', '*'), ('NUMBER', '9'), ('NUMBER', '8'), ('KEYWORD', 'if'), ('IDENTIFIER', 'result1'), ('OPERATOR', '>'), ('NUMBER', '20'), ('IDENTIFIER', 'print'), ('OPERATOR', '('), ('STRING', 'The speed is greater than 20 m/s.'), ('OPERATOR', ')'), ('KEYWORD', 'else'), ('IDENTIFIER', 'print'), ('OPERATOR', '('), ('STRING', 'The speed is not greater than 20 m/s.'), ('OPERATOR', ')'), ('IDENTIFIER', 'count'), ('OPERATOR', '='), ('NUMBER', '0'), ('IDENTIFIER', 'while'), ('IDENTIFIER', 'count'), ('OPERATOR', '<'), ('NUMBER', '5'), ('IDENTIFIER', 'print'), ('OPERATOR', '('), ('STRING', 'Count:'), ('IDENTIFIER', 'count'), ('OPERATOR', ')'), ('IDENTIFIER', 'count'), ('OPERATOR', '+'), ('OPERATOR', '='), ('NUMBER', '1'), ('IDENTIFIER', 'def'), ('IDENTIFIER', 'calculate_energy'), ('OPERATOR', '('), ('IDENTIFIER', 'mass'), ('IDENTIFIER', 'velocity'), ('OPERATOR', ')'), ('IDENTIFIER', 'return'), ('NUMBER', '0'), ('NUMBER', '5'), ('OPERATOR', '*'), ('IDENTIFIER', 'mass'), ('OPERATOR', '*'), ('IDENTIFIER', 'velocity'), ('OPERATOR', '*'), ('OPERATOR', '*'), ('NUMBER', '2'), ('IDENTIFIER', 'energy'), ('OPERATOR', '='), ('IDENTIFIER', 'calculate_energy'), ('OPERATOR', '('), ('NUMBER', '2'), ('NUMBER', '10'), ('OPERATOR', ')'), ('KEYWORD', 'if'), ('IDENTIFIER', 'speed'), ('OPERATOR', '>'), ('NUMBER', '0'), ('IDENTIFIER', 'and'), ('KEYWORD', 'time'), ('OPERATOR', '<'), ('NUMBER', '10'), ('IDENTIFIER', 'print'), ('OPERATOR', '('), ('STRING', 'The object is moving.'), ('OPERATOR', ')'), ('IDENTIFIER', 'elif'), ('KEYWORD', 'time'), ('OPERATOR', '>'), ('OPERATOR', '='), ('NUMBER', '10'), ('IDENTIFIER', 'print'), ('OPERATOR', '('), ('STRING', 'The object has stopped.'), ('OPERATOR', ')'), ('KEYWORD', 'else'), ('IDENTIFIER', 'print'), ('OPERATOR', '('), ('STRING', 'Invalid condition.'), ('OPERATOR', ')')]


# Create a parser instance
parser = Parser(tokens)

# Parse the input stream
parsed_statements = parser.parse()

# Print the parsed statements
for statement in parsed_statements:
    print(statement, '\n')