from Lua import lua


# Base classes for different node types
class Node:...
# Contexts for variable references
class ExprContext(Node):...
class Load(ExprContext):...
class Store(ExprContext):...
# Boolean operations
class BoolOp(Node):...
class And(BoolOp):...
class Or(BoolOp):...
# Binary operators
class Operator(Node):...
class Add(Operator):...
class BitAnd(Operator):...
class BitOr(Operator):...
class BitXor(Operator):...
class Div(Operator):...
class FloorDiv(Operator):...
class LShift(Operator):...
class Mod(Operator):...
class Mult(Operator):...
class MatMult(Operator):...
class Pow(Operator):...
class RShift(Operator):...
class Sub(Operator):...
# Unary operators
class UnaryOp(Node):...
class Invert(UnaryOp):...
class Not(UnaryOp):...
class UAdd(UnaryOp):...
class USub(UnaryOp):...
# Comparison operators
class CmpOp(Node):...
class Eq(CmpOp):...
class Gt(CmpOp):...
class GtE(CmpOp):...
class In(CmpOp):...
class Is(CmpOp):...
class IsNot(CmpOp):...
class Lt(CmpOp):...
class LtE(CmpOp):...

class Chunk(Node):
    def __init__(self, body):
        self.body = body

class Function(Node):
    def __init__(self, name, params, body, is_local=False):
        self.name = name
        self.params = params
        self.body = body
        self.is_local = is_local

class Local(Node):
    def __init__(self, names, values=None):
        self.names = names
        self.values = values

class Assignment(Node):
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value

class If(Node):
    def __init__(self, test, body, orelse=None):
        self.test = test
        self.body = body
        self.orelse = orelse

class While(Node):
    def __init__(self, test, body):
        self.test = test
        self.body = body

class For(Node):
    def __init__(self, var, start, end, step, body):
        self.var = var
        self.start = start
        self.end = end
        self.step = step
        self.body = body

class ForIn(Node):
    def __init__(self, vars, iter, body):
        self.vars = vars
        self.iter = iter
        self.body = body

class Return(Node):
    def __init__(self, values):
        self.values = values

class Break(Node):...
class Expr(Node):
    def __init__(self, value):
        self.value = value

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Call(Node):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class Name(Node):
    def __init__(self, id):
        self.id = id

class Constant(Node):
    def __init__(self, value):
        self.value = value

class Index(Node):
    def __init__(self, value, index):
        self.value = value
        self.index = index

class TableConstructor(Node):
    def __init__(self, fields):
        self.fields = fields

class TableField(Node):
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Require(Node):
    def __init__(self, module):
        self.module = module



class LuaParser:
    def __init__(self, tokens):
        tokens.append(None)
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        token = self.current_token()
        if token is None:
            raise Exception("Unexpected end of input")
        self.pos += 1
        return token

    def parse_chunk(self):
        statements = []
        while self.current_token():
            statements.append(self.parse_statement())
        return Chunk(statements)

    def parse_statement(self):
        token: Token = self.current_token()
        if token.type == lua.token.NAME and token.value == lua.keyword.LOCAL:
            return self.parse_local()
        elif token.type == lua.token.NAME and token.value == lua.keyword.FUNCTION:
            return self.parse_function()
        elif token.type == lua.token.IF:
            return self.parse_if()
        elif token.type == lua.token.WHILE:
            return self.parse_while()
        elif token.type == lua.token.WHILE:
            return self.parse_for()
        elif token.type == lua.token.RETURN:
            return self.parse_return()
        elif token.type == lua.token.BREAK:
            self.consume(lua.token.BREAK)
            return Break()
        else:
            return self.parse_assignment_or_expr()

    def parse_local(self):
        self.consume(lua.token.LOCAL)  # local
        names = [self.consume(lua.token.NAME).value]
        if self.current_token().type == lua.token.OPERATOR and self.current_token().value == lua.object.ASSIGN:
            self.consume(lua.token.OPERATOR)
            values = [self.parse_expr()]
            return Local(names, values)
        return Local(names)

    def parse_function(self):
        self.consume(lua.token.NAME)  # function
        name = self.consume(lua.token.NAME).value
        self.consume("LPAREN")
        params = []
        while self.current_token()["type"] != "RPAREN":
            params.append(self.consume(lua.token.NAME).value)
            if self.current_token()["type"] == "COMMA":
                self.consume("COMMA")
        self.consume("RPAREN")
        body = self.parse_chunk()
        self.consume("END")
        return Function(name, params, body.body, is_local=False)

    def parse_if(self):
        self.consume("IF")
        test = self.parse_expr()
        self.consume("THEN")
        body = self.parse_chunk()
        orelse = []
        if self.current_token()["type"] == "ELSE":
            self.consume("ELSE")
            orelse = self.parse_chunk().body
        self.consume("END")
        return If(test, body.body, orelse)

    def parse_while(self):
        self.consume(lua.token.WHILE)
        test = self.parse_expr()
        self.consume(lua.token.DO)
        body = self.parse_chunk()
        self.consume(lua.token.END)
        return While(test, body.body)

    def parse_for(self):
        self.consume(lua.token.FOR)
        var = self.consume(lua.token.NAME).value
        self.consume(lua.token.OPERATOR)  # =
        start = self.parse_expr()
        self.consume("COMMA")
        end = self.parse_expr()
        step = Constant(1)
        if self.current_token()["type"] == "COMMA":
            self.consume("COMMA")
            step = self.parse_expr()
        self.consume("DO")
        body = self.parse_chunk()
        self.consume("END")
        return For(Name(var), start, end, step, body.body)

    def parse_return(self):
        self.consume("RETURN")
        values = [self.parse_expr()]
        return Return(values)

    def parse_assignment_or_expr(self):
        left = self.parse_expr()
        if self.current_token() and self.current_token()["type"] == lua.token.OPERATOR and self.current_token().value == "=":
            self.consume(lua.token.OPERATOR)
            right = self.parse_expr()
            return Assignment([left], right)
        return Expr(left)

    def parse_expr(self):
        left = self.parse_term()
        while self.current_token() and self.current_token()["type"] == "BIN_OP":
            op = self.consume("BIN_OP").value
            right = self.parse_term()
            left = BinOp(left, self.transform_operator(op), right)
        return left

    def parse_term(self):
        token = self.current_token()
        if token.type == "NUMBER":
            return Constant(float(self.consume("NUMBER").value))
        elif token.type == "STRING":
            return Constant(self.consume("STRING").value[1:-1])
        elif token.type == lua.token.NAME:
            name = self.consume(lua.token.NAME).value
            if self.current_token() and self.current_token()["type"] == "LPAREN":
                self.consume("LPAREN")
                args = []
                while self.current_token()["type"] != "RPAREN":
                    args.append(self.parse_expr())
                    if self.current_token()["type"] == "COMMA":
                        self.consume("COMMA")
                self.consume("RPAREN")
                return Call(Name(name), args)
            return Name(name)
        elif token.type == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expr()
            self.consume("RPAREN")
            return expr
        elif token.type == "LBRACE":
            return self.parse_table_constructor()
        else:
            raise Exception(f"Unexpected token: {token}")

    def parse_table_constructor(self):
        self.consume("LBRACE")
        fields = []
        while self.current_token()["type"] != "RBRACE":
            key = self.consume(lua.token.NAME).value
            self.consume(lua.token.OPERATOR)  # =
            value = self.parse_expr()
            fields.append(TableField(Name(key), value))
            if self.current_token()["type"] == "COMMA":
                self.consume("COMMA")
        self.consume("RBRACE")
        return TableConstructor(fields)

    def transform_operator(self, op):
        operators = {
            "+": Add(),
            "-": Sub(),
            "*": Mult(),
            "/": Div(),
            "%": Mod(),
            "==": Eq(),
            "~=": NotEq(),
            "<=": LtE(),
            ">=": GtE(),
            "<": Lt(),
            ">": Gt(),
            "and": And(),
            "or": Or()
        }
        return operators[op]

