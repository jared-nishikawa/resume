import compiler
import sys

if __name__ == "__main__":
    if not sys.argv[1:] or sys.argv[1] not in {"short", "long"}:
        sys.exit(f"Usage: {sys.argv[0]} [short/long]")

    with open("resume.jn") as f:
        data = f.read()

    c = compiler.Compiler(data)
    c.compile()
    if sys.argv[1] == "short":
        lines = c.generate(long=False)
    elif sys.argv[1] == "long":
        lines = c.generate(long=True)
    with open("resume.tex", "w") as f:
        for line in lines:
            f.write(line + "\n\n")



