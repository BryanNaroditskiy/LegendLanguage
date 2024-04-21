import re
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




# Keywords and operators
keywords = {
    'true', 'false', 'avg', 'max', 'min', 'sort', 'shuffle', 'reverse', 'union', 'intersection',
    'sin', 'cos', 'tan', 'sqrt', 'random', 'lambda', 'if', 'else', 'repeat', 'time',
    'acceleration', 'momentum', 'gravity', 'kinetic_energy', 'potential_energy', 'work', 'power',
    'impulse', 'torque', 'angular_velocity', 'angular_acceleration', 'friction', 'pressure',
    'density', 'moment_of_inertia', 'spring_constant', 'frequency', 'wavelength'
}


# Define the operators mapping
operators = {
    '+': 'ADD', '-': 'SUBTRACT', '*': 'MULTIPLY', '**': 'POWER', '/': 'DIVIDE', '^': 'XOR',
    '%': 'MODULO', '=': 'EQUALS', '!=': 'NOT_EQUALS', '>': 'GREATER_THAN', '<': 'LESS_THAN',
    '>=': 'GREATER_THAN_OR_EQUAL', '<=': 'LESS_THAN_OR_EQUAL', '&&': 'AND', '||': 'OR', '!': 'NOT',
    '(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', ':': 'COLON'
}

# Regular expressions for different token types
identifier_regex = r'[a-zA-Z_][a-zA-Z0-9_]*'
number_regex = r'\d*\.\d+|\d+\.\d*|\d+'
string_regex = r'"(?:[^"\\]|\\.)*"'
comment_regex = r';.*'
special_print_start = r'print\|'
special_print_end = r'\|'
whitespace_regex = r'\s+'

# Combine all regex into one
token_regex = re.compile(
    f'({special_print_start}|{special_print_end}|{string_regex}|{number_regex}|' +
    '|'.join(map(re.escape, operators.keys())) +  # Specific tokens for each operator
    f'|{identifier_regex}|{whitespace_regex}|{comment_regex}|\\n)'
)



# Define the operators mapping
operators = {
    '+': 'ADD', '-': 'SUBTRACT', '*': 'MULTIPLY', '**': 'POWER', '/': 'DIVIDE', '^': 'XOR',
    '%': 'MODULO', '=': 'EQUALS', '!=': 'NOT_EQUALS', '>': 'GREATER_THAN', '<': 'LESS_THAN',
    '>=': 'GREATER_THAN_OR_EQUAL', '<=': 'LESS_THAN_OR_EQUAL', '&&': 'AND', '||': 'OR', '!': 'NOT',
    '(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', ':': 'COLON'
}

# Regular expressions for different token types
identifier_regex = r'[a-zA-Z_][a-zA-Z0-9_]*'
number_regex = r'\d*\.\d+|\d+\.\d*|\d+'
string_regex = r'"(?:[^"\\]|\\.)*"'
comment_regex = r';.*'
special_print_start = r'print\|'
special_print_end = r'\|'
whitespace_regex = r'\s+'

# Combine all regex into one
token_regex = re.compile(
    f'({special_print_start}|{special_print_end}|{string_regex}|{number_regex}|' +
    '|'.join(map(re.escape, operators.keys())) +  # Specific tokens for each operator
    f'|{identifier_regex}|{whitespace_regex}|{comment_regex}|\\n)'
)

# Combine all regex into one
# token_regex = re.compile(
#     f'({"|".join(map(re.escape, keywords))}|{special_print_start}|{special_print_end}|{string_regex}|{number_regex}|' +
#     '|'.join(map(re.escape, operators.keys())) +  # Specific tokens for each operator
#     f'|{identifier_regex}|{whitespace_regex}|{comment_regex}|\\n)'
# )

# Tokenize the code
def lex(code):
    tokens = []
    lines = code.split('\n')  # Split the code into lines
    current_indentation = 0
    for line in lines:
        line_tokens = []
        # Determine the indentation level
        indentation = len(line) - len(line.lstrip())
        while indentation < current_indentation:
            line_tokens.append(('DEDENT', current_indentation))
            current_indentation -= 4
        if indentation > current_indentation:
            line_tokens.append(('INDENT', indentation))
            current_indentation = indentation
        for match in re.finditer(token_regex, line):
            token = match.group().strip()
            if token:
                if token[0] == ';':  # Ignore comments
                    break
                elif token.startswith('print|'):
                    line_tokens.append(('PRINT_START', token))
                elif token == '|':
                    line_tokens.append(('PRINT_END', token))
                elif token in keywords:
                    line_tokens.append(('KEYWORD', token))
                elif token in operators:
                    line_tokens.append((operators[token], token))  # Use specific token for each operator
                elif re.match(number_regex, token):
                    line_tokens.append(('NUMBER', token))
                elif re.match(string_regex, token):
                    line_tokens.append(('STRING', token[1:-1]))  # Remove quotes
                else:
                    line_tokens.append(('IDENTIFIER', token))
        tokens.extend(line_tokens)
        tokens.append(('NEWLINE', '\n'))  # Add a newline token after each line
    return tokens

# Example usage
# code = """
# ; Variable declarations
# speed = 10.5  ; km/h
# distance = 100  ; meters
# t = 2.5  ; seconds
# mass = 5  ; kg
# message = "Hello, Legend!"
#
# ; Conditional statements
# if result1 > 20:
#     print|"The speed is greater than 20 m/s."|
# else:
#     print|"The speed is not greater than 20 m/s."|
# """


tokens = lex(code)
print(tokens)

# Example usage
# code = """
# ; Conditional statements
# if result1 > 20:
#     print|"The speed is greater than 20 m/s."|
# else:
#     print|"The speed is not greater than 20 m/s."|
# """

# tokens = lex(code)
# for token in tokens:
#     print(token)

# for token in tokens:
#     print(token)




class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0
        self.current_token = self.tokens[self.current_token_idx]

    def consume(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]}")

    def advance(self):
        self.current_token_idx += 1
        if self.current_token_idx < len(self.tokens):
            self.current_token = self.tokens[self.current_token_idx]
        else:
            self.current_token = None

    def parse(self):
        statements = []
        while self.current_token:
            print(self.current_token)
            if self.current_token[0] == 'NEWLINE':
                self.advance()  # Skip newline tokens
            elif self.current_token[0] == 'IDENTIFIER':
                statements.append(self.parse_assignment())
            elif self.current_token[0] == 'KEYWORD':
                if self.current_token[1] == 'if':
                    statements.append(self.parse_if_statement())
                elif self.current_token[1] == 'while':
                    statements.append(self.parse_while_loop())
                elif self.current_token[1] == 'def':
                    statements.append(self.parse_function_definition())
                else:
                    raise SyntaxError(f"Invalid keyword: {self.current_token[1]}")
            elif self.current_token[0] == 'PRINT_START':
                statements.append(self.parse_print_statement())
            elif self.current_token[0] == 'COMMENT':
                # Ignore comments
                self.advance()
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")

            # Check if there's more to parse after an if statement
            if statements and statements[-1][0] == 'IF_STATEMENT' and not statements[-1][3]:
                # If the if statement has no else branch, continue parsing
                continue
            elif self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
                # If the current token is an else keyword, return to parse_if_statement to handle the else branch
                return statements

        return statements

    def parse_assignment(self):
        identifier = self.current_token[1]
        self.consume('IDENTIFIER')
        self.consume('EQUALS')  # Ensure the assignment operator is '='

        # Parse the expression
        #print(identifier)
        expression = self.parse_expression()
        #print(expression)

        # Consume the newline token
        self.consume('NEWLINE')

        print(('ASSIGNMENT', identifier, expression))
        return ('ASSIGNMENT', identifier, expression)

    def parse_expression(self):
        print("Parsing expression...")
        expression = self.parse_simple_expression()
        print(expression)

        # Parse binary operations until reaching a newline or a higher precedence operator
        while self.current_token and self.current_token[1] in operators and self.current_token[1] != ':':
            operator = operators[self.current_token[1]]
            print("Operator:", operator)
            self.advance()  # Consume the operator
            next_operand = self.parse_simple_expression()
            print("Next operand:", next_operand)
            expression = (operator, expression, next_operand)

        print("Parsed expression:", expression)
        return expression

    def parse_simple_expression(self):
        # Parse the operand (identifier, number, or string)
        if self.current_token[0] in ('NUMBER', 'IDENTIFIER', 'STRING'):
            expression = self.current_token[1]
            self.advance()
        else:
            raise SyntaxError(f"Invalid expression: {self.current_token[1]}")

        return expression

    def parse_if_statement(self):
        self.consume('KEYWORD')  # if
        condition = self.parse_expression()
        self.consume('COLON')
        self.consume('NEWLINE')

        # Parse true condition statements
        true_statements = self.parse_statements()

        false_statements = []

        # Check for else branch
        if self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
            self.consume('KEYWORD')  # else
            self.consume('COLON')
            self.consume('NEWLINE')

            # Parse false condition statements
            false_statements = self.parse_statements()

        # Return the entire if-else block
        print(('IF_STATEMENT', condition, true_statements, false_statements))
        return ('IF_STATEMENT', condition, true_statements, false_statements)

    def parse_statements(self):
        statements = []
        current_indentation = None

        while self.current_token and self.current_token[0] != 'DEDENT':
            if self.current_token[0] == 'NEWLINE':
                self.advance()  # Skip newline tokens
            elif self.current_token[0] == 'INDENT':
                current_indentation = self.current_token[1]
                self.advance()
            else:
                if self.current_token[0] == 'DEDENT':
                    break
                if current_indentation is not None and self.current_token[1] != current_indentation:
                    raise IndentationError("Inconsistent indentation")

                statements.append(self.parse())

        return statements

    def parse_while_loop(self):
        self.consume('KEYWORD')  # while
        condition = self.parse_expression()
        self.consume('COLON')
        self.consume('NEWLINE')
        loop_statements = self.parse()
        return ('WHILE_LOOP', condition, loop_statements)

    def parse_function_definition(self):
        self.consume('KEYWORD')  # def
        function_name = self.current_token[1]
        self.consume('IDENTIFIER')
        self.consume('LEFT_PAREN')
        parameters = []
        while self.current_token[0] == 'IDENTIFIER':
            parameters.append(self.current_token[1])
            self.consume('IDENTIFIER')
            if self.current_token[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RIGHT_PAREN')
        self.consume('COLON')
        self.consume('NEWLINE')
        function_body = self.parse()
        return ('FUNCTION_DEFINITION', function_name, parameters, function_body)

    def parse_print_statement(self):
        self.consume('PRINT_START')
        value = self.parse_expression()
        self.consume('PRINT_END')
        self.consume('NEWLINE')
        print(('PRINT', value))
        return ('PRINT', value)


# Example usage
parser = Parser(lex(code))
print(parser.current_token)
statements = parser.parse()
for statement in statements:
    print(statement)

