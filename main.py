import re

# Token types
keywords = {
    'true', 'false', 'avg', 'max', 'min', 'sort', 'shuffle', 'reverse', 'union', 'intersection',
    'sin', 'cos', 'tan', 'sqrt', 'random', 'lambda', 'if', 'else', 'repeat', 'time',
    'acceleration', 'momentum', 'gravity', 'kinetic_energy', 'potential_energy', 'work', 'power',
    'impulse', 'torque', 'angular_velocity', 'angular_acceleration', 'friction', 'pressure',
    'density', 'moment_of_inertia', 'spring_constant', 'frequency', 'wavelength'
}

operators = {'+', '-', '*', '**', '/', '^', '%', '=', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '(', ')'}

# Regular expressions
identifier_regex = r'[a-zA-Z_][a-zA-Z0-9_]*'
number_regex = r'\d*\.\d+|\d+\.\d*|\d+'
string_regex = r'"(?:[^"\\]|\\.)*"'
comment_regex = r';.*'
special_print_start = r'print\|'
special_print_end = r'\|'
whitespace_regex = r'\s+'

# Updated token regex
token_regex = re.compile(
    f'({special_print_start}|{special_print_end}|{string_regex}|{number_regex}|'
    f'{"|".join(map(re.escape, operators))}|{identifier_regex}|{whitespace_regex}|{comment_regex})'
)

def lex(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        token = match.group().strip()
        if token:
            if token[0] == ';':  # Ignore comments
                continue
            elif token.startswith('print|'):
                tokens.append(('PRINT_START', token))
            elif token == '|':
                tokens.append(('PRINT_END', token))
            elif token in keywords:
                tokens.append(('KEYWORD', token))
            elif token in operators:
                tokens.append(('OPERATOR', token))
            elif re.match(number_regex, token):
                tokens.append(('NUMBER', token))
            elif re.match(string_regex, token):
                tokens.append(('STRING', token[1:-1]))  # Remove quotes
            else:
                tokens.append(('IDENTIFIER', token))
    #print(tokens)
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0

    def parse(self):
        statements = []
        while self.current_token_idx < len(self.tokens):
            print(f"Current token: {self.tokens[self.current_token_idx]}")
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self):
        token_type, token_value = self.peek()
        print(f"Current token in parse_statement: {token_type} {token_value}")
        if token_type == 'PRINT_START':
            return self.parse_print_statement()
        elif token_type == 'IDENTIFIER' and self.peek_ahead()[1] == '=':
            return self.parse_assignment_statement()
        else:
            self.error("Unexpected token")

    def parse_print_statement(self):
        self.consume('PRINT_START')  # Consume the 'print|'
        values = []
        while True:
            token_type, token_value = self.peek()
            if token_type == 'PRINT_END':
                break
            values.append(token_value)
            self.advance()
        self.consume('PRINT_END')  # Consume the '|'
        return ('PRINT', values)

    def parse_assignment_statement(self):
        identifier = self.consume('IDENTIFIER')[1]
        self.consume('OPERATOR', '=')
        token_type, token_value = self.peek()
        if token_type == 'NUMBER':
            value = self.consume('NUMBER')[1]
        elif token_type == 'STRING':
            value = self.consume('STRING')[1]
        elif token_type == 'IDENTIFIER':
            value = self.consume('IDENTIFIER')[1]
        else:
            self.error("Expected a number or string for assignment")
        return ('ASSIGN', identifier, value)

    def peek(self):
        if self.current_token_idx < len(self.tokens):
            return self.tokens[self.current_token_idx]
        else:
            return None, None

    def peek_ahead(self):
        if self.current_token_idx + 1 < len(self.tokens):
            return self.tokens[self.current_token_idx + 1]
        else:
            return None, None

    def consume(self, expected_type, expected_value=None):
        token_type, token_value = self.tokens[self.current_token_idx]
        if token_type != expected_type or (expected_value is not None and token_value != expected_value):
            self.error(f"Expected {expected_type}{' with value ' + expected_value if expected_value else ''}, got {token_type}{' with value ' + token_value if token_value else ''}")
        self.current_token_idx += 1
        return token_type, token_value

    def advance(self):
        self.current_token_idx += 1

    def error(self, message):
        raise SyntaxError(message)


class CodeGenerator:
    def __init__(self, statements):
        self.statements = statements

    def generate_code(self):
        output = []
        for statement in self.statements:
            if statement[0] == 'PRINT':
                output.append('print(' + ', '.join(map(str, statement[1])) + ')')
            elif statement[0] == 'ASSIGN':
                output.append(f'{statement[1]} = {statement[2]}')
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
; Variable declarations
speed = 10.5  ; km/h
distance = 100  ; meters
t = 2.5  ; seconds
mass = 5  ; kg
message = "Hello, Legend!"

; Arithmetic operations
result1 = distance / t
result2 = speed * t
result3 = mass * 9.8  ; gravitational constant

; Conditional statements
if result1 > 20:
    print|"The speed is greater than 20 m/s."|
else:
    print|"The speed is not greater than 20 m/s."|

; Looping
count = 0
while count < 5:
    print|"Count:", count|
    count += 1

; Function definition
def calculate_energy|mass, velocity|:
    return 0.5 * mass * velocity**2

; Function call
energy = calculate_energy|2, 10|

; Reserved words usage
if speed > 0 and t < 10:
    print|"The object is moving."|
elif t >= 10:
    print|"The object has stopped."|
else:
    print|"Invalid condition."|

; Comments
; This is a single-line comment
"""

print("Starting...")
compiled_code = compile_legend(code)
print("Compiled Code:")
print(compiled_code)
