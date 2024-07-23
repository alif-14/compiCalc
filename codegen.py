class CodeGenerator:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.temp_count = 0
        self.code = []
        self.var_address = {}

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate_code(self):
        for statement in self.parse_tree:
            if statement[0] == 'ASSIGN':
                var_name = statement[1]
                expression = self.evaluate_expression(statement[2])
                if expression.startswith("t"):  # if the expression is a temp variable
                    self.code.append(f"(= , {expression} , , {var_name})")
                else:  # it's a constant or variable
                    temp_var = self.new_temp()
                    self.code.append(f"(= , {expression} , , {temp_var})")
                    self.code.append(f"(= , {temp_var} , , {var_name})")
            elif statement[0] == 'PRINT':
                var_name = statement[1]
                self.code.append(f"(p , {var_name} , , )")
        return self.code

    def evaluate_expression(self, expr):
        if isinstance(expr, (int, float)):  # Handle numeric literals
            return f"#{int(expr)}"
        elif isinstance(expr, str):  # Handle identifiers
            return expr
        elif isinstance(expr, tuple):
            if len(expr) == 2 and expr[0] in ('SIN', 'COS'):
                func = expr[0].lower()
                arg = self.evaluate_expression(expr[1])
                temp_var = self.new_temp()
                self.code.append(f"({func} , {arg} , , {temp_var})")
                return temp_var
            elif len(expr) == 3:
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                temp_var = self.new_temp()
                if expr[0] == 'PLUS':
                    self.code.append(f"(+ , {left} , {right} , {temp_var})")
                elif expr[0] == 'MINUS':
                    self.code.append(f"(- , {left} , {right} , {temp_var})")
                elif expr[0] == 'TIMES':
                    self.code.append(f"(* , {left} , {right} , {temp_var})")
                elif expr[0] == 'DIVIDE':
                    self.code.append(f"(/ , {left} , {right} , {temp_var})")
                elif expr[0] == 'POWER':
                    self.code.append(f"(** , {left} , {right} , {temp_var})")
                return temp_var
        raise ValueError(f"Invalid expression: {expr}")

