def is_whitespace(c):
    return c in {" ", "\t", "\n", "\r", "\v"}

special = {
        ",": "comma",
        ":": "colon",
        "{": "leftcurly",
        "}": "rightcurly",
        "[": "leftsquare",
        "]": "rightsquare",
        "*": "asterisk",
        }

keywords = {
        "data",
        }

class Token:
    def __init__(self, index, value, t, row, col):
        self.index = index
        self.value = value
        self.type = t
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{{value={self.value}, type={self.type}}}"

class Scanner:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.tokens = []
        self.row = 0
        self.col = 0

    def peek(self, n=0):
        if self.index+n >= len(self.text):
            return '\0'
        return self.text[self.index+n]

    def read(self):
        if self.index >= len(self.text):
            return "\0"
        c = self.text[self.index]
        self.index += 1
        if c == '\n':
            self.row += 1
            self.col = 0
        else:
            self.col += 1
        return c

    def create_token(self):
        i = self.index
        v = self.read()
        t = special[v]
        return Token(i, v, t, self.row, self.col)

    def read_whitespace(self):
        i = self.index
        v = ""
        while is_whitespace(self.peek()):
            v += self.read()
        return Token(i, v, "whitespace", self.row, self.col)

    def read_string(self):
        i = self.index
        v = ""
        self.read()
        while self.peek() != '"':
            v += self.read()
        self.read()
        return Token(i, v, "string", self.row, self.col)

    def read_token(self):
        i = self.index
        v = ""
        while (not is_whitespace(self.peek())) and (self.peek() not in special):
            v += self.read()
        if v in keywords:
            return Token(i, v, v, self.row, self.col)
        return Token(i, v, "identifier", self.row, self.col)

    def read_comment(self):
        self.read()
        c = self.read()
        if c == "/":
            line = ""
            while 1:
                a = self.peek()
                if a == "\n":
                    break
                line += a
                self.read()
            return Token(self.index, line, "comment", self.row, self.col)
        elif c == "*":
            chunk = ""
            while 1:
                a = self.peek()
                b = self.peek(1)
                if a+b == "*/":
                    self.read()
                    self.read()
                    break
                chunk += self.read()
            return Token(self.index, chunk, "comment", self.row, self.col)

    def scan_token(self):
        c = self.peek()

        if c == "\0":
            return Token(self.index, "\0", "eof", self.row, self.col)
        if is_whitespace(c):
            return self.read_whitespace()
        if c == '"':
            return self.read_string()
        if c == "/":
            return self.read_comment()
        if c in special:
            return self.create_token()
        return self.read_token()

    def scan(self):
        while 1:
            t = self.scan_token()
            if t.type == "eof":
                break
            if t.type == "whitespace":
                continue
            self.tokens.append(t)

if __name__ == "__main__":
    with open("resume.jn") as f:
        data = f.read()

    s = Scanner(data)
    s.scan()
    print(s.tokens)


