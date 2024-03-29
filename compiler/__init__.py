import compiler.parser as parser
import compiler.template as template

class CompilerError(BaseException):
    pass

class Compiler:
    def __init__(self, text):
        p = parser.Parser(text)
        p.parse()
        self.exprs = p.exprs
        self.data_exprs = {}
        self.decl_exprs = {}

    def verify_decl(self, decl_expr):
        if decl_expr.name not in self.data_exprs:
            raise CompilerError(f"unknown identifier: {decl_expr.name}")
        data_expr = self.data_exprs[decl_expr.name]
        for a in decl_expr.decl_map:
            if a not in data_expr.attrs and a not in data_expr.opt_attrs:
                raise CompilerError(f"attribute not found for {decl_expr.name}: {a}")
        for a in data_expr.attrs:
            if a not in decl_expr.decl_map:
                raise CompilerError(f"{decl_expr.name} must contain attribute: {a}")

    def compile(self):
        for e in self.exprs:
            if e.type == "data":
                self.data_exprs[e.name] = e
            elif e.type == "decl":
                self.verify_decl(e)
                if e.name not in self.decl_exprs:
                    self.decl_exprs[e.name] = []
                self.decl_exprs[e.name].append(e)

    def generate(self, long=True):
        t = template.Template()

        # header
        t.cmd("documentclass", "letter")
        t.cmd("usepackage", "geometry", flags=["margin=0.5in"])
        t.cmd("usepackage", "parskip")
        t.cmd("begin", "document")
        t.cmd("newcommand", template.cmd("vspc"), template.cmd("vskip5mm"))
        t.cmd("renewcommand" + template.cmd("labelitemi", template.cmd("raisebox", "0.25ex", template.cmd("tiny" + template.mathmode(template.cmd("bullet"))))))
        t.cmd("pagenumbering", "gobble")
        t.cmd("textbf", template.cmd("Huge", "Jared Nishikawa, PhD"))
        t.cmd("texttt", "jared.nishikawa@gmail.com")

        if long:

            t.cmd("large", "Summary")
            t.cmd("vskip1mm")
            t.cmd("hrule")
    
            for e in self.decl_exprs["SummaryEntry"]:
                blob = e.decl_map["blob"]
                t.plain(blob)

        t.cmd("large", "Experience")
        t.cmd("vskip1mm")
        t.cmd("hrule")

        for e in self.decl_exprs["ExperienceEntry"]:
            name = e.decl_map["name"]
            start = e.decl_map["startdate"]
            end = e.decl_map["enddate"]
            title = e.decl_map["title"]
            t.cmd("textbf", f"{name} " + template.cmd("hfill") + f" {start} - {end}")
            t.plain(title)
            if long:
                t.cmd("begin", "itemize")
                t.cmd("setlength" + template.cmd("itemsep", "-0.5em"))
                for item in e.decl_map["projects"]:
                    t.cmd("item " + item)
                t.cmd("end", "itemize")

        t.cmd("vspc")
        t.cmd("large", "Talks")
        t.cmd("vskip1mm")
        t.cmd("hrule")

        for e in self.decl_exprs["TalksEntry"]:
            conf = e.decl_map["conference"]
            loc = e.decl_map["location"]
            date = e.decl_map["date"]
            title = e.decl_map["title"]
            t.cmd("textbf", f"{conf} ({loc}) " + template.cmd("hfill") + f" {date}")
            t.cmd("textit", title)

        t.cmd("vspc")
        t.cmd("large", "Education")
        t.cmd("vskip1mm")
        t.cmd("hrule")

        for e in self.decl_exprs["EducationEntry"]:
            degree = e.decl_map["degree"]
            major = e.decl_map["major"]
            school = e.decl_map["school"]
            start = e.decl_map["startdate"]
            end = e.decl_map["enddate"]
            t.cmd("textbf", f"{degree}, {major} - {school} " + template.cmd("hfill") + f" {start} - {end}")
            if long:
                if not any(key in e.decl_map for key in ["thesis", "advisor"]):
                    continue

                t.cmd("begin", "itemize")
                t.cmd("setlength" + template.cmd("itemsep", "-0.5em"))
                for key in ["thesis", "advisor"]:
                    if key in e.decl_map:
                        value = e.decl_map[key]
                        if key == "thesis":
                            t.cmd(f"item {key.capitalize()}: " + template.cmd("textit", value))
                        else:
                            t.cmd(f"item {key.capitalize()}: {value}")
                t.cmd("end", "itemize")

        t.cmd("vspc")
        t.cmd("large", "Skills")
        t.cmd("vskip1mm")
        t.cmd("hrule")

        for e in self.decl_exprs["SkillsEntry"]:
            typ = e.decl_map["type"]
            l = e.decl_map["list"]
            t.cmd("textbf", typ)
            t.plain(l)

        t.cmd("end", "document")
        return t.lines

    def generate_long():
        pass

if __name__ == "__main__":
    with open("resume.jn") as f:
        data = f.read()

    c = Compiler(data)
    c.compile()
    c.generate_short()


