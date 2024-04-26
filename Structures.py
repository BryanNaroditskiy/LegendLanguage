import re

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
