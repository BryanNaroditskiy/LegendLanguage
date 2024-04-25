import re
import math
# Example usage
code = """
; Variable declarations
speed = 10.5  ; km/h
distance = 100  ; meters
t = 2.5  ; seconds
mass = 5  ; kg
message = "Hello, Legend!"
print|'message'|

;keyword/function testing
max_test = max|9, 8|
min_test = min|2, 3|
sin_test = sin|45|
cos_test = cos|45|
tan_test = tan|45|
sqrt_test = sqrt|81|
momentum_test = momentum|2, 3|
ke_test = kinetic_energy|2, 4|
pe_test = potential_energy|2, 5|
work_test = work|2, 2| ;4
power_test = power|10, 5|
impulse_test = impulse|2, 5|
torque_test = torque|2, 3|
ang_vel_test = angular_velocity|pi, 2|
ang_accel_test = angular_acceleration|pi, 2|
friction_test = friction|0.5, 10|
pressure_test = pressure|100, 10|
density_test = density|50, 10|
moment_of_inertia_test = moment_of_inertia|10, 5|
spring_test = spring_constant|20, 2|
frequency_test = frequency|2|
wavelength_test = wavelength|10, 2|



print|max_test|
print|min_test|
; Arithmetic operations
result1 = distance / t
print|result1|
result2 = speed * t
result3 = mass * gravity  ; gravitational constant

; Conditional statements
if result1 > 20:
    print|"The speed is greater than 20 m/s."|
else:
    print|"The speed is not greater than 20 m/s."|

; Looping
count = 0
while count < 5:
    print|"Count:", count|
    count = count + 1

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
    'true', 'false', 'max', 'min','sin', 'cos', 'tan', 'sqrt', 'if', 'else', 'while', 'def',
    'print', 'momentum', 'gravity', 'kinetic_energy', 'potential_energy', 'work', 'power',
    'impulse', 'torque', 'angular_velocity', 'angular_acceleration', 'friction', 'pressure',
    'density', 'moment_of_inertia', 'spring_constant', 'frequency', 'wavelength', 'return', 'pi'
}





# Define the operators mapping
operators = {
    '+=': 'INCREMENT', '**': 'POWER', '|': 'PIPE', '+': 'ADD', '-': 'SUBTRACT', '*': 'MULTIPLY', '/': 'DIVIDE', '^': 'XOR',
    '%': 'MODULO', '=': 'EQUALS', '!=': 'NOT_EQUALS', '>': 'GREATER_THAN', '<': 'LESS_THAN',
    '>=': 'GREATER_THAN_OR_EQUAL', '<=': 'LESS_THAN_OR_EQUAL', '&&': 'AND', '||': 'OR', '!': 'NOT',
    '(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', ':': 'COLON'
}

# Regular expressions for different token types
identifier_regex = r'[a-zA-Z_][a-zA-Z0-9_]*'
number_regex = r'\d*\.\d+|\d+\.\d*|\d+'
string_regex = r'"(?:[^"\\]|\\.)*"'
comment_regex = r';.*'
whitespace_regex = r'\s+'

# Combine all regex into one
token_regex = re.compile(
    f'(|{string_regex}|{number_regex}|' +
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
                # elif token.startswith('print|'):
                #     line_tokens.append(('PRINT_START', token))
                # elif token == '|':
                #     line_tokens.append(('PRINT_END', token))
                elif token in keywords:
                    if token == 'gravity':
                        line_tokens.append(('NUMBER', '9.8'))  # Replace 'gravity' keyword with its numeric value
                    elif token == 'pi':
                        line_tokens.append(('NUMBER', '3.14'))
                    elif token == 'print':
                        line_tokens.append(("PRINT", token))
                    elif token == 'max':
                        line_tokens.append(('MAX', token))  # Token for start of max() function call
                    elif token == 'min':
                        line_tokens.append(('MIN', token))
                    elif token == 'sin':
                        line_tokens.append(('SIN', token))
                    elif token == 'tan':
                        line_tokens.append(('TAN', token))
                    elif token == 'cos':
                        line_tokens.append(('COS', token))
                    elif token == 'kinetic_energy':
                        line_tokens.append(('KINETIC_ENERGY', token))
                    elif token == 'potential_energy':
                        line_tokens.append(('POTENTIAL_ENERGY', token))
                    elif token == 'work':
                        line_tokens.append(('WORK', token))
                    elif token == 'momentum':
                        line_tokens.append(('MOMENTUM', token))
                    elif token == 'power':
                        line_tokens.append(('POWER', token))
                    elif token == 'impulse':
                        line_tokens.append(('IMPULSE', token))
                    elif token == 'torque':
                        line_tokens.append(('TORQUE', token))
                    elif token == 'angular_velocity':
                        line_tokens.append(('ANGULAR_VELOCITY', token))
                    elif token == 'angular_acceleration':
                        line_tokens.append(('ANGULAR_ACCELERATION', token))
                    elif token == 'friction':
                        line_tokens.append(('FRICTION', token))
                    elif token == 'pressure':
                        line_tokens.append(('PRESSURE', token))
                    elif token == 'density':
                        line_tokens.append(('DENSITY', token))
                    elif token == 'moment_of_inertia':
                        line_tokens.append(('MOMENT_OF_INERTIA', token))
                    elif token == 'spring_constant':
                        line_tokens.append(('SPRING_CONSTANT', token))
                    elif token == 'frequency':
                        line_tokens.append(('FREQUENCY', token))
                    elif token == 'wavelength':
                        line_tokens.append(('WAVELENGTH', token))
                    elif token == 'sqrt':
                        line_tokens.append(('SQUARE_ROOT', token))
                    elif token == '|':
                        line_tokens.append(('PIPE', token))
                    # elif token == '(':
                    #     line_tokens.append(('LEFT_PAREN', token))
                    # elif token == ')':
                    #     line_tokens.append(('RIGHT_PAREN', token))
                    elif token == ',':
                        line_tokens.append(('COMMA', token))
                    else:
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



tokens = lex(code)
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

    def advance(self):
        self.current_token_idx += 1
        if self.current_token_idx < len(self.tokens):
            self.current_token = self.tokens[self.current_token_idx]
        else:
            self.current_token = None

    def parse(self):
        statements = []
        current_indentation = 0  # Track the current indentation level

        while self.current_token:
            print(self.current_token)
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
            elif self.current_token[0] == 'IDENTIFIER':
                statements.append(self.parse_assignment())
            elif self.current_token[0] == 'KEYWORD':
                if self.current_token[1] == 'if':
                    statements.append(self.parse_if_statement())
                elif self.current_token[1] == 'while':
                    statements.append(self.parse_while_loop())
                    self.advance()
                elif self.current_token[1] == 'def':
                    statements.append(self.parse_function_definition())
                    self.advance()
                elif self.current_token[1] == 'else':
                    print("reached else")
                    return statements  # Return the 'else' keyword to parse_if_statement
                else:
                    raise SyntaxError(f"Invalid keyword: {self.current_token[1]}")
            elif self.current_token[0] == 'PRINT':
                statements.append(self.parse_print_statement())
            elif self.current_token[0] == 'COMMENT':
                # Ignore comments
                self.advance()
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
            print("test parse", statements)
            # Check if there's more to parse after an if statement
            if statements and statements[-1][0] == 'IF_STATEMENT' and not statements[-1][3]:
                # If the if statement has no else branch, continue parsing
                continue
            elif self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
                # If the current token is an else keyword, return to parse_if_statement to handle the else branch
                break

        return statements

    def parse_assignment(self):
        identifier = self.current_token[1]
        print(identifier)
        self.consume('IDENTIFIER')
        print("assign", self.current_token)
        if self.current_token[0] == 'EQUALS':
            self.consume('EQUALS')  # Ensure the assignment operator is '='

            # Parse the expression
            print(self.current_token)
            expression = self.parse_expression()

            # Consume the newline token
            self.consume('NEWLINE')

            print(('ASSIGNMENT', identifier, expression))
            return ('ASSIGNMENT', identifier, expression)

        elif self.current_token[0] == 'INCREMENT':
            self.consume('INCREMENT')  # Consume the '+=' token

            # Construct the expression for +=
            increment_expression = self.parse_expression()

            # Construct the expression for the augmented assignment
            expression = ('ADD', identifier, increment_expression)

            # Consume the newline token
            self.consume('NEWLINE')

            print("increment", ('ASSIGNMENT', identifier, expression))
            return ('ASSIGNMENT', identifier, expression)

    def parse_expression(self):
        print("Parsing expression...")

        if self.current_token[0] in ('MAX', 'MIN', 'WORK', 'POWER', 'IMPULSE', 'TORQUE', 'ANGULAR_VELOCITY', 'ANGULAR_ACCELERATION', 'FRICTION', 'PRESSURE', 'DENSITY', 'MOMENT_OF_INERTIA', 'SPRING_CONSTANT', 'WAVELENGTH', 'MOMENTUM', 'KINETIC_ENERGY', 'POTENTIAL_ENERGY'):
            keyword = self.current_token[0]
            self.advance()  # Consume 'max'
            self.consume('PIPE')  # Consume '('
            print(self.current_token)
            arguments = [self.parse_simple_expression()]  # Parse the first argument
            print(arguments)
            while self.current_token[0] == 'NUMBER':
                arguments.append(self.parse_simple_expression())  # Parse additional arguments

            self.consume('PIPE')  # Consume ')'
            return (keyword, arguments)  # Return tuple for max function call
            # Parse the left operand
        if self.current_token[0] in ('SIN', 'COS', 'TAN', 'SQUARE_ROOT', 'FREQUENCY'):
            keyword = self.current_token[0]
            self.advance()
            self.consume('PIPE')
            arguments = self.parse_simple_expression()
            self.consume('PIPE')
            return (keyword, arguments)



        left_operand = self.parse_simple_expression()
        print("Left operand:", left_operand)


        # Parse binary operations until reaching a newline or a higher precedence operator
        while self.current_token and self.current_token[1] in operators and self.current_token[0] not in (
                'COLON', 'AND', 'OR'):
            operator = operators[self.current_token[1]]
            print("Operator:", operator)
            self.advance()  # Consume the operator
            next_operand = self.parse_simple_expression()
            print("Next operand:", next_operand)
            left_operand = (operator, left_operand, next_operand)
            print("Updated expression:", left_operand)

        print("Parsed expression:", left_operand)

        # Check if there's an 'AND' keyword
        if self.current_token and self.current_token[0] == 'AND':
            keyword = self.current_token[0]
            self.advance()  # Consume the 'AND' token

            right_operand = self.parse_simple_expression()
            # Parse the right operand
            while self.current_token and self.current_token[1] in operators and self.current_token[0] not in (
                    'COLON', 'AND', 'OR'):
                operator = operators[self.current_token[1]]
                print("Operator:", operator)
                self.advance()  # Consume the operator
                next_operand = self.parse_simple_expression()
                print("Next operand:", next_operand)
                right_operand = (operator, right_operand, next_operand)
                print("Updated expression:", left_operand)

            # Create the expression tuple
            left_operand = (keyword, left_operand, right_operand)
            print("tag", left_operand)
        return left_operand


    def parse_simple_expression(self):
        # Parse the operand (identifier, number, or string)
        if self.current_token[0] in ('NUMBER', 'IDENTIFIER', 'STRING'):
            expression = self.current_token
            self.advance()
        else:
            raise SyntaxError(f"Invalid expression: {self.current_token[1]}")

        return expression

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

        # Parse the function body statements
        function_body = []

        while self.current_token and self.current_token[0] != 'DEDENT':
            if self.current_token[0] == 'NEWLINE':
                self.advance()  # Skip newline tokens
            elif self.current_token[0] == 'INDENT':
                self.advance()  # Skip the indentation token
            elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'return':
                function_body.append(self.parse_return_statement())
            else:
                # Parse the statement if it has the same or lower indentation level
                function_body.append(self.parse())
        return ('FUNCTION_DEFINITION', function_name, parameters, function_body)

    def parse_return_statement(self):
        self.consume('KEYWORD')  # return
        if self.current_token[0] != 'NEWLINE':
            value = self.parse_expression()  # Parse the expression after return
        else:
            value = None  # If there's no value after return, set it to None
        self.consume('NEWLINE')  # Consume the newline token
        return ('RETURN_STATEMENT', value)

    def parse_function_call(self):
        function_name = self.current_token[1]  # Get the function name
        self.consume('IDENTIFIER')  # Consume the function name token
        self.consume('LEFT_PAREN')  # Consume the left parenthesis '('

        arguments = []  # List to store function arguments

        # Parse function arguments
        while self.current_token[0] != 'RIGHT_PAREN':
            arguments.append(self.parse_expression())  # Parse each argument
            if self.current_token[0] == 'COMMA':
                self.consume('COMMA')  # Consume the comma between arguments

        self.consume('RIGHT_PAREN')  # Consume the right parenthesis ')'
        self.consume('NEWLINE')  # Consume the newline token

        return ('FUNCTION_CALL', function_name, arguments)

    def parse_print_statement(self):
        self.consume('PRINT')
        self.consume('PIPE')
        value = self.parse_print_expression()
        print("print", value)
        self.consume('PIPE')
        self.consume('NEWLINE')
        print(('PRINT', value))
        return ('PRINT', value)


# Example usage


parser = Parser(lex(code))
print(parser.current_token)
statements = parser.parse()


print("End of Run")
for statement in statements:
    print(statement)
class Interpreter:
    @staticmethod
    def interpret(parsed_statements):
        python_code = ""

        for statement in parsed_statements:
            if statement[0] == 'ASSIGNMENT':
                python_code += f"{statement[1]} = {Interpreter._interpret_expression(statement[2])}\n"
            elif statement[0] == 'IF_STATEMENT':
                condition = Interpreter._interpret_expression(statement[1])
                if_block = Interpreter._interpret_block(statement[2][0])
                else_block = Interpreter._interpret_block(statement[3][0])
                python_code += f"if {condition}:\n"
                python_code += if_block
                if else_block:
                    python_code += "else:\n"
                    python_code += else_block
            elif statement[0] == 'WHILE_LOOP':
                condition = Interpreter._interpret_expression(statement[1])
                loop_block = Interpreter._interpret_block(statement[2][0])
                python_code += f"while {condition}:\n"
                python_code += loop_block
            elif statement[0] == 'PRINT':
                python_code += f"print("
                for item in statement[1]:
                    if item[0] == 'STRING':
                        python_code += f"'{item[1]}'"
                    elif item[0] == 'IDENTIFIER':
                        python_code += item[1]
                    elif item[0] == 'NUMBER':
                        python_code += item[1]
                    if item != statement[1][-1]:
                        python_code += ", "
                python_code += ")\n"

        return python_code
    @staticmethod
    def execute_python_code(python_code):
        exec(python_code)
    @staticmethod
    def _interpret_expression(expression):
        if expression[0] == 'NUMBER' or expression[0] == 'STRING':
            if expression[0] == 'STRING':
                return "'"+ expression[1] + "'"
            return float(expression[1])
        elif expression[0] == 'IDENTIFIER':
            return expression[1]
        elif expression[0] == 'ADD':
            return f"{Interpreter._interpret_expression(expression[1])} + {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'SUBTRACT':
            return f"{Interpreter._interpret_expression(expression[1])} - {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'MULTIPLY':
            return f"{Interpreter._interpret_expression(expression[1])} * {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'DIVIDE':
            return f"{Interpreter._interpret_expression(expression[1])} / {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'GREATER_THAN':
            return f"{Interpreter._interpret_expression(expression[1])} > {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'LESS_THAN':
            return f"{Interpreter._interpret_expression(expression[1])} < {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'AND':
            return f"{Interpreter._interpret_expression(expression[1])} and {Interpreter._interpret_expression(expression[2])}"
        elif expression[0] == 'MAX':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return max(values)
        elif expression[0] == 'MIN':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return min(values)
        elif expression[0] == 'SQUARE_ROOT':
            arguments = expression[1]
            values = Interpreter._interpret_expression(arguments)
            return math.sqrt(values)
        elif expression[0] == 'SIN':
            arguments = expression[1]
            values = Interpreter._interpret_expression(arguments)
            values = math.radians(values)
            return math.sin(values)
        elif expression[0] == 'COS':
            arguments = expression[1]
            values = Interpreter._interpret_expression(arguments)
            values = math.radians(values)
            return math.cos(values)
        elif expression[0] == 'TAN':
            arguments = expression[1]
            values = Interpreter._interpret_expression(arguments)
            values = math.radians(values)
            return math.tan(values)
        elif expression[0] == 'KINETIC_ENERGY':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return 0.5 * values[0] * values[1] ** 2 #Assumes first value is mass & second is velocity (joules)
        elif expression[0] == 'POTENTIAL_ENERGY':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0] * values[1] * 9.8 #assumes first value is mass and second is height (joules)
        elif expression[0] == 'WORK':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0] * values[1] # force * displacement (Joules)
        elif expression[0] == 'POWER':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #work/time (Watts)
        elif expression[0] == 'IMPULSE':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0] * values[1] #force * delta_time (joules)
        elif expression[0] == 'TORQUE':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0] * values[1] #moment_arm * force (joules)
        elif expression[0] == 'ANGULAR_VELOCITY':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #delta_theta/delta time (radians per second)
        elif expression[0] == 'ANGULAR_ACCELERATION':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #delta_omega/delta_time (radians per second squared)
        elif expression[0] == 'FRICTION':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #mu * normal_force (fricitional force in newtons)
        elif expression[0] == 'PRESSURE':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #force/area (pascals)
        elif expression[0] == 'DENSITY':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #mass/volume (in kilograms per cubic meter)
        elif expression[0] == 'MOMENT_OF_INERTIA':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0] * values[1] ** 2 #mass * radius (in  kilogram square meters)
        elif expression[0] == 'SPRING_CONSTANT':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #force/displacement (newtons per meter)
        elif expression[0] == 'FREQUENCY':
            arguments = expression[1]
            values = Interpreter._interpret_expression(arguments)
            return 1/values #period (in hertz)
        elif expression[0] == 'WAVELENGTH':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0]/values[1] #speed/frequency in hertz
        elif expression[0] == 'MOMENTUM':
            arguments = expression[1]
            values = [Interpreter._interpret_expression(arg) for arg in arguments]
            return values[0] * values[1]









    @staticmethod
    def _interpret_block(block):
        python_code = ""
        for statement in block:
            if statement[0] == 'PRINT':
                python_code += f"    print("
                for item in statement[1]:
                    if item[0] == 'STRING':
                        python_code += f"'{item[1]}'"
                    elif item[0] == 'IDENTIFIER':
                        python_code += item[1]
                    elif item[0] == 'NUMBER':
                        python_code += item[1]
                    if item != statement[1][-1]:
                        python_code += ", "
                python_code += ")\n"
            elif statement[0] == 'ASSIGNMENT':
                python_code += f"    {statement[1]} = {Interpreter._interpret_expression(statement[2])}\n"
        return python_code


python_code = Interpreter.interpret(statements)
print(python_code)
Interpreter.execute_python_code(python_code)
