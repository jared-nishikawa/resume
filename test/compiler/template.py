def cmd(command, *args, flags=[]):
    text = ""
    text += f"\\{command}"
    for flag in flags:
        text += f"[{flag}]"
    for arg in args:
        text += f"{{{arg}}}"
    return text

def mathmode(s):
    return f"${s}$"


class Template:
    def __init__(self):
        self.lines = []

    def cmd(self, command, *args, flags=[]):
        self.lines.append(cmd(command, *args, flags=flags))

