import re
# Example usage
line_of_code = 'x+1 > "Ay want to see something cool?"'



code2 = """
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
    
; Reserved words usage
if speed > 0 && t < 10:
    print|"The object is moving."|
else:
    print|"Invalid condition."|

; Comments
; This is a single-line comment
"""


# Keywords and operators
keywords = {
    'true', 'false', 'avg', 'max', 'min', 'sort', 'shuffle', 'reverse', 'union', 'intersection',
    'sin', 'cos', 'tan', 'sqrt', 'random', 'lambda', 'if', 'else', 'while', 'repeat', 'time', 'def',
    'acceleration', 'momentum', 'gravity', 'kinetic_energy', 'potential_energy', 'work', 'power',
    'impulse', 'torque', 'angular_velocity', 'angular_acceleration', 'friction', 'pressure',
    'density', 'moment_of_inertia', 'spring_constant', 'frequency', 'wavelength', 'return'
}


# Define the operators mapping
operators = {
    '+=': 'INCREMENT', '**': 'POWER', '+': 'ADD', '-': 'SUBTRACT', '*': 'MULTIPLY', '/': 'DIVIDE', '^': 'XOR',
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


tokens = lex(line_of_code)
print(tokens)


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

    # def advance(self):
    #     self.current_token_idx += 1
    #     if self.current_token_idx < len(self.tokens):
    #         self.current_token = self.tokens[self.current_token_idx]
    #     else:
    #         self.current_token = None

    def advance(self):
        if len(self.tokens) > 0:
            self.tokens.pop(0)
            if len(self.tokens) > 0:
                self.current_token = self.tokens[0]

    def parse(self):
        if len(self.tokens) > 0:
            #statements = []
            current_indentation = 0  # Track the current indentation level

            while self.current_token:
                if self.current_token[0] == 'NEWLINE':
                    self.advance()  # Skip newline tokens
                elif self.current_token[0] == 'INDENT':
                    # Increase the current indentation level
                    current_indentation += 1
                    self.advance()  # Skip the indentation token
                elif self.current_token[0] == 'DEDENT':
                    # Decrease the current indentation level
                    #current_indentation -= 1
                    break
                elif self.current_token[0] == 'KEYWORD':
                    if self.current_token[1] == 'if':
                        return self.parse_if_statement()
                    # TODO Make this work with recursion
                    # elif self.current_token[1] == 'while':
                    #     return self.parse_while_loop()
                    # elif self.current_token[1] == 'else':
                    #     print("reached else")
                    #     return statements  # Return the 'else' keyword to parse_if_statement
                    else:
                        raise SyntaxError(f"Invalid keyword: {self.current_token[1]}")

                # Parsing single tokens
                elif (len(self.tokens) == 1) or self.tokens[1][0] == 'NEWLINE':
                    return self.current_token
                # Parse arithmatic expressions
                elif self.current_token[0] in ['NUMBER', 'IDENTIFIER']:
                    try:
                        left = int(self.current_token[1])
                    except:
                        left = self.current_token[1]
                    self.advance()
                    if self.current_token[0] in operators.values():
                        operation = self.current_token[0]
                        self.advance()
                        if self.current_token[0] not in operators.values():
                            try:
                                right = int(self.current_token[1])
                            except:
                                right = self.current_token[1]
                            expression = (operation, left, right)

                            # Check if next token is an operator
                            self.advance()
                            while self.current_token and (self.current_token[0] in operators.values()):
                                operation = self.current_token[0]

                                self.advance()
                                if operation in ['LESS_THAN', 'GREATER_THAN']:
                                    try:
                                        operand = self.parse()
                                    except:
                                        raise SyntaxError(f"{operation} is not followed by and operand.")
                                    expression = (operation, expression, operand)
                                    self.advance()
                                elif self.current_token[0] not in operators.values():
                                    try:
                                        operand = int(self.current_token[1])
                                    except:
                                        operand = self.current_token[1]
                                    expression = (operation, expression, operand)
                                    self.advance()
                                else:
                                    raise SyntaxError(f"Invalid operation ('{operation}', {expression}, '{self.current_token[0]}')")

                            print(expression)
                            return expression
                        else:
                            raise SyntaxError(f"Invalid operation ('{operation}', {left}, '{self.current_token[0]}')")

                elif self.current_token[0] == 'PRINT_START':
                    return self.parse_print_statement()
                elif self.current_token[0] == 'COMMENT':
                    # Ignore comments
                    self.advance()
                else:
                    raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
                # Check if there's more to parse after an if statement
                # if statements and statements[-1][0] == 'IF_STATEMENT' and not statements[-1][3]:
                #     # If the if statement has no else branch, continue parsing
                #     continue
                # elif self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
                #     # If the current token is an else keyword, return to parse_if_statement to handle the else branch
                #     break

    def parse_print_expression(self):
        # Parse the operand (identifier, number, string, or composite expression)
        expression = []

        # Keep parsing until we encounter a token that doesn't match either string or identifier
        while self.current_token[0] in ('STRING', 'IDENTIFIER'):
            # Check if the current token is a string
            if self.current_token[0] == 'STRING':
                expression.append(self.current_token)  # Add the string token to the expression
                self.advance()  # Move to the next token

            # Check if the current token is an identifier
            elif self.current_token[0] == 'IDENTIFIER':
                expression.append(self.current_token)  # Add the identifier token to the expression
                self.advance()  # Move to the next token

        # If the expression is empty, it means we didn't encounter any strings or identifiers
        if not expression:
            raise SyntaxError(f"Invalid expression: {self.current_token[1]}")

        return expression

    def parse_if_statement(self):
        self.consume('KEYWORD')  # if
        condition = self.parse_expression()
        self.consume('COLON')
        self.consume('NEWLINE')

        # Parse true condition statements
        print("here", self.current_token)
        true_statements = self.parse_statements()
        print(true_statements)

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
        current_indentation = 0

        while self.current_token and self.current_token[0] != 'DEDENT':
            print("statement current", self.current_token)
            if self.current_token[0] == 'NEWLINE':
                self.advance()  # Skip newline tokens
            elif self.current_token[0] == 'INDENT':
                # Increase the current indentation level
                current_indentation += 1
                self.advance()  # Skip the indentation token
            elif self.current_token[0] == 'DEDENT':
                break
            else:
                # Parse the statement
                print(self.current_token)
                statement = self.parse()
                print("test state", statement)
                statements.append(statement)

        # Check if we've reached the end of the block
        if self.current_token and self.current_token[0] == 'DEDENT':
            # Decrease the current indentation level
            current_indentation -= 1
            self.advance()
            # Return to the parse_if_statement function
            return statements

        return statements

    def parse_while_loop(self):
        self.consume('KEYWORD')  # while
        condition = self.parse_expression()
        self.consume('COLON')
        self.consume('NEWLINE')

        loop_statements = []
        current_indentation = 0
        print("while testing", self.current_token)

        # Parse statements inside the while loop until dedent is encountered
        while self.current_token and self.current_token[0] != 'DEDENT':
            if self.current_token[0] == 'NEWLINE':
                self.advance()  # Skip newline tokens
            elif self.current_token[0] == 'INDENT':
                current_indentation += 1
                self.advance()  # Skip the indentation token
            elif self.current_token[0] == 'DEDENT':
                break
            else:
                # Check the indentation level of the current token
                # token_indentation = len(self.current_token[1]) // 4
                # if token_indentation > current_indentation:
                #     raise IndentationError("Unexpected indentation level")

                # Parse the statement if it has the same or lower indentation level
                loop_statements.append(self.parse())

        return ('WHILE_LOOP', condition, loop_statements)

    def parse_return_statement(self):
        self.consume('KEYWORD')  # return
        if self.current_token[0] != 'NEWLINE':
            value = self.parse_expression()  # Parse the expression after return
        else:
            value = None  # If there's no value after return, set it to None
        self.consume('NEWLINE')  # Consume the newline token
        return ('RETURN_STATEMENT', value)

    def parse_print_statement(self):
        self.consume('PRINT_START')
        value = self.parse_print_expression()
        print("print", value)
        self.consume('PRINT_END')
        self.consume('NEWLINE')
        print(('PRINT', value))
        return ('PRINT', value)


# Example usage
parser = Parser(lex(line_of_code))
paser_output = parser.parse()
