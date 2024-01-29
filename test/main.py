import compiler
import sys

if __name__ == "__main__":
    if not sys.argv[1:]:
        sys.exit(f"Usage: {sys.argv[0]} [short/long]")

    with open("resume.jn") as f:
        data = f.read()

    c = compiler.Compiler(data)
    c.compile()
    if sys.argv[1] == "short":
        lines = c.generate_short()
        with open("short.tex", "w") as f:
            for line in lines:
                f.write(line + "\n\n")


