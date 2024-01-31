import compiler
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["short", "long"])
    parser.add_argument("--in", required=True, help="in file", dest="infile")
    parser.add_argument("--out", default="resume.tex", dest="outfile")
    args = parser.parse_args()

    with open(args.infile) as f:
        data = f.read()

    c = compiler.Compiler(data)
    c.compile()
    if args.type == "short":
        lines = c.generate(long=False)
    elif args.type == "long":
        lines = c.generate(long=True)
    with open(args.outfile, "w") as f:
        for line in lines:
            f.write(line + "\n\n")



