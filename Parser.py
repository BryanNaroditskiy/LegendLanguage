import Structures

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
        while self.current_token and self.current_token[1] in Structures.operators and self.current_token[0] not in (
                'COLON', 'AND', 'OR'):
            operator = Structures.operators[self.current_token[1]]
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
            while self.current_token and self.current_token[1] in Structures.operators and self.current_token[0] not in (
                    'COLON', 'AND', 'OR'):
                operator = Structures.operators[self.current_token[1]]
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
