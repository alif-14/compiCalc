import math

class Evaluator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.symbol_table = {}

    def evaluate(self):
        results = []
        with open(self.input_file, 'r') as file:
            for line in file:
                line = line.strip().strip(';')
                    
                if line.startswith("print"):
                    var_name = line[line.find('(') + 1 : line.find(')')].strip()
                    if var_name in self.symbol_table:
                        results.append(self.symbol_table[var_name])
                    else:
                        raise ValueError(f"Variable '{var_name}' not found in symbol table")
                elif line:
                    self.execute(line)
                else:
                    print("line can not be empty, proceeding... (ignoring the line)")
        return results

    def execute(self, line):
        parts = line.split('=')
        if len(parts) == 2:
            target = parts[0].strip()
            expr = parts[1].strip()
            self.symbol_table[target] = eval(expr, {"__builtins__": None}, {"sin": math.sin, "cos": math.cos, **self.symbol_table})
        else:
            raise ValueError(f"Invalid line format: {line}")

