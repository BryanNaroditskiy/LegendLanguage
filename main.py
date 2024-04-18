import re

# Token types
keywords = {
    'true', 'false', 'avg', 'max', 'min', 'sort', 'shuffle', 'reverse', 'union', 'intersection',
    'sin', 'cos', 'tan', 'sqrt', 'random', 'lambda', 'if', 'else', 'repeat', 'time',
    'acceleration', 'momentum', 'gravity', 'kinetic_energy', 'potential_energy', 'work', 'power',
    'impulse', 'torque', 'angular_velocity', 'angular_acceleration', 'friction', 'pressure',
    'density', 'moment_of_inertia', 'spring_constant', 'frequency', 'wavelength'
}

operators = {'+', '-', '*', '/', '^', '%', '=', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '(', ')'}

# Regular expressions
identifier_regex = r'[a-zA-Z_][a-zA-Z0-9_]*'
number_regex = r'\d+'
string_regex = r'"(?:[^"\\]|\\.)*"'
comment_regex = r';.*'
whitespace_regex = r'\s+'

token_regex = re.compile(f'({identifier_regex}|{number_regex}|{string_regex}|'
                         f'{"|".join(map(re.escape, operators))}|{whitespace_regex}|{comment_regex})')


def lex(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        token = match.group().strip()
        if token:
            if token[0] == ';':  # Ignore comments
                continue
            elif token in keywords:
                tokens.append(('KEYWORD', token))
            elif token in operators:
                tokens.append(('OPERATOR', token))
            elif re.match(number_regex, token):
                tokens.append(('NUMBER', token))
            elif re.match(r'"[^"]*"', token):  # Adjusted to recognize string literals
                tokens.append(('STRING', token[1:-1]))  # Remove quotes
            else:
                tokens.append(('IDENTIFIER', token))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0

    def parse(self):
        statements = []
        while self.current_token_idx < len(self.tokens):
            print("Current token:", self.tokens[self.current_token_idx])
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
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
        else:
            self.error("Unexpected token")

    def parse_print_statement(self):
        self.consume('KEYWORD', 'print')
        values = []
        while self.peek()[0] != 'COMMENT':
            token_type, token_value = self.peek()
            if token_type == 'STRING' or token_type == 'NUMBER':
                values.append(token_value)
            elif token_type == 'IDENTIFIER':
                values.append(token_value)
            else:
                self.error("Unexpected token in print statement")
            self.advance()
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
        value = self.parse_expression()  # Parse expression instead of NUMBER
        return ('ASSIGN', identifier, value)

    def parse_expression(self):
        expr = []
        while self.current_token_idx < len(self.tokens) and self.peek()[1] not in {')', ';'}:
            token_type, token_value = self.peek()
            if token_type in {'NUMBER', 'IDENTIFIER'}:
                expr.append(token_value)
            elif token_value in operators:
                expr.append(token_value)
            self.advance()  # Advance the token index here to consume tokens
        return ' '.join(expr)

    def parse_block(self):
        block = []
        self.consume('OPERATOR', '{')
        while self.peek()[1] != '}':
            block.append(self.parse_statement())
        self.consume('OPERATOR', '}')
        return block

    def consume(self, expected_type, expected_value=None):
        token_type, token_value = self.tokens[self.current_token_idx]
        if token_type != expected_type or (expected_value is not None and token_value != expected_value):
            self.error(
                f"Expected {expected_type}{' with value ' + expected_value if expected_value else ''}, got {token_type}{' with value ' + token_value if token_value else ''}")
        self.current_token_idx += 1
        return token_type, token_value

    def peek(self):
        if self.current_token_idx < len(self.tokens):
            return self.tokens[self.current_token_idx]
        else:
            return None, None

    def advance(self):
        self.current_token_idx += 1

    def error(self, message):
        raise SyntaxError(message)


class CodeGenerator:
    def __init__(self, statements):
        self.statements = statements

    def generate_code(self):
        output = []
        indent_level = 0
        for statement in self.statements:
            if statement[0] == 'PRINT':
                output.append(' '.join(map(str, statement[1])))
            elif statement[0] == 'ASSIGN':
                output.append(' ' * (indent_level * 2) + f'{statement[1]} = {statement[2]}')
            elif statement[0] == 'IF':
                output.append(' ' * (indent_level * 2) + f'if {statement[1]}:')
                indent_level += 1
                output.extend([' ' * (indent_level * 2) + line for line in statement[2]])
                indent_level -= 1
            elif statement[0] == 'REPEAT':
                output.append(' ' * (indent_level * 2) + f'for _ in range({statement[1]}):')
                indent_level += 1
                output.extend([' ' * (indent_level * 2) + line for line in statement[2]])
                indent_level -= 1
        return '\n'.join(output)


def compile_legend(code):
    tokens = lex(code)
    print("Lexed")
    parser = Parser(tokens)
    print("Starting parser...")
    statements = parser.parse()
    print("Parsed")
    code_generator = CodeGenerator(statements)
    print("Generated")
    compiled_code = code_generator.generate_code()
    print("Compiled")
    return compiled_code


# Example usage
code = """
x = 5
print "Hello, World!"
"""

print("Starting...")
compiled_code = compile_legend(code)
print("Compiled Code:")
print(compiled_code)
