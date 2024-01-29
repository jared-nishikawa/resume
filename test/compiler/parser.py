import compiler.scanner as scanner

class ParserError(BaseException):
    pass

class Expr:
    def __init__(self, t):
        self.type = t

    def __repr__(self):
        return f"{self.type}"

class DataExpr(Expr):
    def __init__(self, name, attrs):
        super().__init__("data")
        self.name = name
        self.attrs = set(attrs)

    def __repr__(self):
        return f"{self.name}-{self.attrs}"

class DeclExpr(Expr):
    def __init__(self, name, decl_map):
        super().__init__("decl")
        self.name = name
        self.decl_map = decl_map

    def __repr__(self):
        return f"{self.name}-{self.decl_map}"

class EOFExpr(Expr):
    def __init__(self):
        super().__init__("eof")


class Parser:
    def __init__(self, text):
        s = scanner.Scanner(text)
        s.scan()
        self.tokens = s.tokens
        self.index = 0
        self.exprs = []

    def peek(self, n=0):
        if self.index+n >= len(self.tokens):
            return scanner.Token(self.index, "\0", "eof")
        return self.tokens[self.index+n]

    def read(self):
        if self.index >= len(self.tokens):
            return scanner.Token(self.index, "\0", "eof")
        tok = self.tokens[self.index]
        self.index += 1
        return tok

    def expect(self, t):
        tok = self.read()
        if tok.type != t:
            raise ParserError(f"expected {t}, found {tok.type}")
        return tok

    def parse_data(self):
        self.expect("data")
        name = self.expect("identifier").value
        self.expect("leftcurly")
        attrs = []
        while 1:
            if self.peek().type == "rightcurly":
                break
            a = self.expect("identifier")
            self.expect("comma")
            attrs.append(a.value)
        self.expect("rightcurly")
        return DataExpr(name, attrs)

    def parse_decl(self):
        name = self.expect("identifier").value
        self.expect("leftcurly")
        decl_map = {}
        while 1:
            if self.peek().type == "rightcurly":
                break
            a = self.expect("identifier")
            self.expect("colon")
            s = self.expect("string")
            self.expect("comma")
            decl_map[a.value] = s.value
        self.expect("rightcurly")
        return DeclExpr(name, decl_map)

    def parse_expr(self):
        t = self.peek()
        if t.type == "eof":
            return Expr("eof")
        if t.type == "identifier":
            return self.parse_decl()
        if t.type == "data":
            return self.parse_data()
        raise ParserError("unhandled")

    def parse(self):
        while 1:
            e = self.parse_expr()
            if e.type == "eof":
                break
            self.exprs.append(e)

if __name__ == "__main__":
    with open("resume.jn") as f:
        data = f.read()

    p = Parser(data)
    p.parse()
    print(p.exprs)
