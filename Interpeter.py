import math


class Interpreter:

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

    def execute_python_code(python_code):
        exec(python_code)

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