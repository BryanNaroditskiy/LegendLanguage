import Structures
import re

def lex(code,):
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
        for match in re.finditer(Structures.token_regex, line):
            token = match.group().strip()
            if token:
                if token[0] == ';':  # Ignore comments
                    break
                # elif token.startswith('print|'):
                #     line_tokens.append(('PRINT_START', token))
                # elif token == '|':
                #     line_tokens.append(('PRINT_END', token))
                elif token in Structures.keywords:
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
                elif token in Structures.operators:
                    line_tokens.append((Structures.operators[token], token))  # Use specific token for each operator
                elif re.match(Structures.number_regex, token):
                    line_tokens.append(('NUMBER', token))
                elif re.match(Structures.string_regex, token):
                    line_tokens.append(('STRING', token[1:-1]))  # Remove quotes
                else:
                    line_tokens.append(('IDENTIFIER', token))
        tokens.extend(line_tokens)
        tokens.append(('NEWLINE', '\n'))  # Add a newline token after each line
    return tokens