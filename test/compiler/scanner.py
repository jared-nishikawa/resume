def is_whitespace(c):
    return c in {" ", "\t", "\n", "\r", "\v"}

special = {
        ",": "comma",
        ":": "colon",
        "{": "leftcurly",
        "}": "rightcurly",
        }

keywords = {
        "data",
        }

class Token:
    def __init__(self, index, value, t):
        self.index = index
        self.value = value
        self.type = t

    def __repr__(self):
        return f"{{value={self.value}, type={self.type}}}"

class Scanner:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.tokens = []

    def peek(self, n=0):
        if self.index+n >= len(self.text):
            return '\0'
        return self.text[self.index+n]

    def read(self):
        if self.index >= len(self.text):
            return "\0"
        c = self.text[self.index]
        self.index += 1
        return c

    def create_token(self):
        i = self.index
        v = self.read()
        t = special[v]
        return Token(i, v, t)

    def read_whitespace(self):
        i = self.index
        v = ""
        while is_whitespace(self.peek()):
            v += self.read()
        return Token(i, v, "whitespace")

    def read_string(self):
        i = self.index
        v = ""
        self.read()
        while self.peek() != '"':
            v += self.read()
        self.read()
        return Token(i, v, "string")

    def read_token(self):
        i = self.index
        v = ""
        while (not is_whitespace(self.peek())) and (self.peek() not in special):
            v += self.read()
        if v in keywords:
            return Token(i, v, v)
        return Token(i, v, "identifier")

    def scan_token(self):
        c = self.peek()

        if c == "\0":
            return Token(self.index, "\0", "eof")
        if is_whitespace(c):
            return self.read_whitespace()
        if c == '"':
            return self.read_string()
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


