from collections import deque

class Parser:
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.popleft()
        else:
            self.current_token = ('EOF', '', 0)

    def parse(self):
        stmts = self.stmts()
        return stmts

    def stmts(self):
        stmts = []
        while self.current_token[0] != 'EOF':
            stmt = self.stmt()
            stmts.append(stmt)
            if self.current_token[0] == 'SEMI':
                self.next_token()
            else:
                raise SyntaxError(f"Expected ';' at line {self.current_token[2]}")
        return stmts

    def stmt(self):
        if self.current_token[0] == 'ID':
            id_token = self.current_token
            self.next_token()
            if self.current_token[0] == 'ASSIGN':
                self.next_token()
                expr = self.expr()
                if self.current_token[0] == 'SEMI':
                    #self.next_token()
                    return ('ASSIGN', id_token[1], expr)
                else:
                    raise SyntaxError(f"Expected ';' at line {self.current_token[2]}")
        elif self.current_token[0] == 'PRINT':
            self.next_token()
            if self.current_token[0] == 'LPAREN':
                self.next_token()
                id_token = self.current_token
                if id_token[0] == 'ID':
                    self.next_token()
                    if self.current_token[0] == 'RPAREN':
                        self.next_token()
                        if self.current_token[0] == 'SEMI':
                            #self.next_token()
                            return ('PRINT', id_token[1])
                        else:
                            raise SyntaxError(f"Expected ';' at line {self.current_token[2]}")
        raise SyntaxError(f"Unexpected token '{self.current_token[1]}' at line {self.current_token[2]}")

    def expr(self):
        term = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token
            self.next_token()
            term = (op[0], term, self.term())
        return term

    def term(self):
        factor = self.factor()
        while self.current_token[0] in ('TIMES', 'DIVIDE', 'POWER'):
            op = self.current_token
            self.next_token()
            factor = (op[0], factor, self.factor())
        return factor

    def factor(self):
        if self.current_token[0] == 'ID':
            factor = self.current_token[1]  # Return identifier
            self.next_token()
        elif self.current_token[0] == 'NUM':
            factor = float(self.current_token[1])  # Return number
            self.next_token()
        elif self.current_token[0] in ('SIN', 'COS'):
            func = self.current_token[0]
            self.next_token()
            if self.current_token[0] == 'LPAREN':
                self.next_token()
                arg = self.expr()
                if self.current_token[0] == 'RPAREN':
                    self.next_token()
                    factor = (func, arg)
                else:
                    raise SyntaxError(f"Expected ')' at line {self.current_token[2]}")
            else:
                raise SyntaxError(f"Expected '(' after '{func.lower()}' at line {self.current_token[2]}")
        elif self.current_token[0] == 'LPAREN':
            self.next_token()
            factor = self.expr()
            if self.current_token[0] == 'RPAREN':
                self.next_token()
            else:
                raise SyntaxError(f"Expected ')' at line {self.current_token[2]}")
        else:
            raise SyntaxError(f"Unexpected token '{self.current_token[1]}' at line {self.current_token[2]}")
        return factor

