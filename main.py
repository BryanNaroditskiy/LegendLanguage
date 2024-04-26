import Parser
import LexicalAnalyzer
import Interpeter

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

def start_main(code_snippet):
    parser = Parser.Parser(LexicalAnalyzer.lex(code_snippet))
    parsed_code = parser.parse()
    python_code = Interpeter.Interpreter.interpret(parsed_code)
    Interpeter.Interpreter.execute_python_code(python_code)

start_main(code)