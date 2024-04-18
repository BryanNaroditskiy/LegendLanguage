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


# Example usage
input_stream = """
; Variable declarations
speed = 10.5  ; km/h
distance = 100  ; meters
time = 2.5  ; seconds
mass = 5  ; kg
message = "Hello, Legend!"

; Arithmetic operations
result1 = distance / time
result2 = speed * time
result3 = mass * 9.8  ; gravitational constant

; Conditional statements
if result1 > 20:
    print("The speed is greater than 20 m/s.")
else:
    print("The speed is not greater than 20 m/s.")

; Looping
count = 0
while count < 5:
    print("Count:", count)
    count += 1

; Function definition
def calculate_energy(mass, velocity):
    return 0.5 * mass * velocity**2

; Function call
energy = calculate_energy(2, 10)

; Reserved words usage
if speed > 0 and time < 10:
    print("The object is moving.")
elif time >= 10:
    print("The object has stopped.")
else:
    print("Invalid condition.")

; Comments
; This is a single-line comment
"""

print(lex(input_stream))
# reserved_words = {'true', 'false', 'avg', 'max', 'min', 'sort', 'shuffle', 'reverse', 'union', 'intersection',
#                   'sin', 'cos', 'tan', 'sqrt', 'random', 'lambda', 'if', 'else', 'repeat', 'time',
#                   'acceleration', 'momentum', 'gravity', 'kinetic_energy', 'potential_energy', 'work',
#                   'power', 'impulse', 'torque', 'angular_velocity', 'angular_acceleration', 'friction',
#                   'pressure', 'density', 'moment_of_inertia', 'spring_constant', 'frequency', 'wavelength',
#                   'damping_coefficient', 'print', 'while', 'def'}  # Reserved words from the Legend language specification
