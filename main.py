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


# Todo
# Redo parser so that it makes expressions like this (eqE (sym x) (int 2)) when it see's an expression
# No need for if or loop statements
# DO NOT DO FUNCTIONS FOR THE SAKE OF OUR SANITY
# Build interpet function to interpet what was parsed
# Make enviroments to keep track of values assigned to each one
# Should be a terminal that when you type our legend language into it will output the result of the code
#
# Ex. Of how it should work:
# parse('10/2') returns  (divE (numE 10) (numE 2))
# exp =  (divE (numE 10) (numE 2))
# interpret(exp) returns (numV 5)
# program outputs '5' for input 10/2
# Program terminal
# >> 10/2
# << 5
class Environment:
    def __init__(self, parent=None):
        self.variables = {}  # Variable list
        self.parent = parent  # Parent of the variable

    def define(self, name, value):  # Defines a new variable in the enviroment list to keep track of it
        self.variables[name] = value

    def assign(self, name, value):  # Assign a value to the variable in the environment
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"Variable '{name}' is not defined.")

    def get(self, name):  # Retrieve variable
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' is not defined.")

    def __str__(self):  # Displays environment list as a string for debugging purposes
        env = self
        env_str = ""
        while env:
            env_str += str(env.variables) + " -> "
            env = env.parent
        return env_str.rstrip(" -> ")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0

    def parse(self):
        statements = []
        while self.current_token_idx < len(self.tokens):
            if self.peek() is None:
                break
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self):
        token_type, token_value = self.peek()
        print(f"Current token in parse_statement: {token_type} {token_value}")  # Detailed debug output
        if token_type == 'PRINT_START':
            return self.parse_print_statement()
        elif token_type == 'IDENTIFIER' and self.peek_ahead() and self.peek_ahead()[1] == '=':
            return self.parse_assignment_statement()
        elif token_type == 'KEYWORD':
            return self.parse_keyword_statement(token_value)  # Handle keywords like if, else, etc.
        else:
            self.advance()  # Move to the next token if not handled
            return None

    def parse_keyword_statement(self, keyword):
        # Placeholder for keyword-specific parsing logic
        self.advance()  # Advance past the keyword
        return (keyword.upper(), [])

    def parse_print_statement(self):
        self.consume('PRINT_START')  # Consume the 'print|'
        values = []
        while True:
            if self.peek()[0] == 'PRINT_END':
                break
            values.append(self.peek()[1])
            self.advance()
        self.consume('PRINT_END')  # Consume the '|'
        return ('PRINT', values)

    def parse_assignment_statement(self):
        identifier = self.consume('IDENTIFIER')[1]
        self.consume('OPERATOR', '=')
        value = self.parse_expression()  # Parse the full expression
        return ('ASSIGN', identifier, value)

    def parse_if_statement(self):
        self.consume('KEYWORD', 'if')  # Assuming 'if' starts the statement
        condition = self.parse_expression()  # Parse the condition expression

        # Expecting a colon or similar to mark the end of the condition
        self.consume('OPERATOR', ':')

        # Assuming the body is correctly parsed as a list of statements
        body = self.parse_block()

        # Debug outputs
        print(f"Condition parsed: {condition}")
        print(f"Body parsed: {body}")

        if not body:  # Ensure body is not empty
            body = []

        return 'IF', condition, body

    def parse_expression(self):
        # TODO
        # Make this recursive so every time it sees a new operator it goes down a level and assigns the values to the right of it to this operator till it sees another operator and when it finishes it goes up a level and assigns everything to the value on the left
        expr = []
        while self.current_token_idx < len(self.tokens) and self.tokens[self.current_token_idx][0] not in {'COMMENT', 'KEYWORD', 'PRINT_START', 'PRINT_END'}:
            token_type, token_value = self.peek()
            print(f"Current token: {token_type} {token_value}")  # Debug each part of the expression
            expr.append(token_value)
            self.advance()
        return ' '.join(expr)

    def parse_block(self):
        body = []
        initial_indent = self.current_indent_level  # Placeholder for current indentation

        while True:
            # Check for end of block by dedent or explicit block end
            if self.check_end_of_block():
                break

            statement = self.parse_statement()
            if statement:
                body.append(statement)

        return body

    def peek(self):
        if self.current_token_idx < len(self.tokens):
            return self.tokens[self.current_token_idx]
        else:
            return None

    def peek_ahead(self):
        if self.current_token_idx + 1 < len(self.tokens):
            return self.tokens[self.current_token_idx + 1]
        else:
            return None

    def consume(self, expected_type, expected_value=None):
        token_type, token_value = self.tokens[self.current_token_idx]
        if token_type != expected_type or (expected_value is not None and token_value != expected_value):
            self.error(f"Expected {expected_type}{' with value ' + expected_value if expected_value else ''}, got {token_type}{' with value ' + token_value if token_value else ''}")
        self.advance()
        return token_type, token_value

    def advance(self):
        if self.current_token_idx < len(self.tokens):
            print(f"Current token: {self.tokens[self.current_token_idx]}")
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
                output.append(self.handle_print(statement))
            elif statement[0] == 'ASSIGN':
                output.append(f"{statement[1]} = {statement[2]}")
            elif statement[0] == 'IF':
                output.append(self.handle_if(statement))
            elif statement[0] == 'WHILE':
                output.append(self.handle_while(statement))
            elif statement[0] == 'FUNCTION_DEF':
                output.append(self.handle_function_def(statement))
            elif statement[0] == 'FUNCTION_CALL':
                output.append(self.handle_function_call(statement))
            # Add more cases as needed for other statement types
        return '\n'.join(output)

    def handle_print(self, statement):
        # Converts print statement to Python print function
        return 'print(' + ', '.join(map(str, statement[1])) + ')'

    def handle_if(self, statement):
        if len(statement) < 3:
            raise ValueError(f"Expected 'IF' statement to have at least 3 elements, got {len(statement)}: {statement}")

        condition = statement[1]
        body = '\n    '.join(self.generate_code(statement[2]))

        return f"if {condition}:\n    {body}"

    def handle_while(self, statement):
        # Handles while loops
        condition = statement[1]
        body = '\n    '.join(self.generate_code(statement[2]))
        return f"while {condition}:\n    {body}"

    def handle_function_def(self, statement):
        # Handles function definition
        func_name = statement[1]
        params = ', '.join(statement[2])
        body = '\n    '.join(self.generate_code(statement[3]))
        return f"def {func_name}({params}):\n    {body}"

    def handle_function_call(self, statement):
        # Handles function calls
        func_name = statement[1]
        args = ', '.join(statement[2])
        return f"{func_name}({args})"


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
