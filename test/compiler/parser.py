import compiler.scanner as scanner

class ParserError(BaseException):
    pass

class Expr:
    def __init__(self, t):
        self.type = t

    def __repr__(self):
        return f"{self.type}"

class CommentExpr(Expr):
     def __init__(self):
        super().__init__("comment")

class DataExpr(Expr):
    def __init__(self, name, attrs, opt_attrs):
        super().__init__("data")
        self.name = name
        self.attrs = set(attrs)
        self.opt_attrs = set(opt_attrs)

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
            return scanner.Token(self.index, "\0", "eof", 0, 0)
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
            raise ParserError(f"expected {t}, found {tok.type} at ({tok.row}, {tok.col})")
        return tok

    def unexpected(self, t):
        raise ParserError(f"unexpected at ({t.row}, {t.col}): {t.value}")

    def parse_data(self):
        self.expect("data")
        name = self.expect("identifier").value
        self.expect("leftcurly")
        attrs = []
        opt_attrs = []
        while 1:
            opt = False
            if self.peek().type == "rightcurly":
                break
            if self.peek().type == "asterisk":
                self.read()
                opt = True
            a = self.expect("identifier")
            self.expect("comma")
            if opt:
                opt_attrs.append(a.value)
            else:
                attrs.append(a.value)
        self.expect("rightcurly")
        return DataExpr(name, attrs, opt_attrs)

    def parse_list(self):
        self.expect("leftsquare")
        values = []
        while 1:
            if self.peek().type == "rightsquare":
                break
            s = self.expect("string")
            values.append(s.value)
            self.expect("comma")
        self.expect("rightsquare")
        return values

    def parse_decl(self):
        name = self.expect("identifier").value
        self.expect("leftcurly")
        decl_map = {}
        while 1:
            if self.peek().type == "rightcurly":
                break
            a = self.expect("identifier")
            self.expect("colon")
            t = self.peek()
            if t.type == "string":
                self.read()
                v = t.value
            elif t.type == "leftsquare":
                v = self.parse_list()
            else:
                self.unexpected(t)
            self.expect("comma")
            decl_map[a.value] = v
        self.expect("rightcurly")
        return DeclExpr(name, decl_map)

    def parse_comment(self):
        self.expect("comment")
        return CommentExpr()

    def parse_expr(self):
        t = self.peek()
        if t.type == "eof":
            return Expr("eof")
        if t.type == "identifier":
            return self.parse_decl()
        if t.type == "data":
            return self.parse_data()
        if t.type == "comment":
            return self.parse_comment()
        raise ParserError(f"unhandled: {t}")

    def parse(self):
        while 1:
            e = self.parse_expr()
            if e.type == "eof":
                break
            if e.type == "comment":
                continue
            self.exprs.append(e)

if __name__ == "__main__":
    with open("resume.jn") as f:
        data = f.read()

    p = Parser(data)
    p.parse()
    print(p.exprs)
