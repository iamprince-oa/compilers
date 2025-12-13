import sys
import os

# valid opcodes and token types
VALID_OPCODES = {
    "load",
    "loadI",
    "store",
    "add",
    "sub",
    "mult",
    "lshift",
    "rshift",
    "output",
    "nop",
}
TOKEN_TYPES = {"OPCODE", "REGISTER", "CONSTANT", "COMMA", "ASSIGN_ARROW", "COMMENT"}


# Scanner Function
def scan_file(path):
    tokens = []
    with open(path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip("\n")
            pos = 0
            while pos < len(line):
                c = line[pos]

                if c.isspace():
                    pos += 1
                    continue

                # comment
                if line[pos : pos + 2] == "//":
                    tokens.append((line_num, "COMMENT", line[pos:]))
                    break
                elif line[pos : pos + 2] == "||":
                    tokens.append((line_num, "COMMENT", line[pos:]))
                    break

                # register
                if c == "r":
                    start = pos
                    pos += 1
                    while pos < len(line) and line[pos].isdigit():
                        pos += 1
                    tokens.append((line_num, "REGISTER", line[start:pos]))
                    continue

                # constant
                if c.isdigit():
                    start = pos
                    while pos < len(line) and line[pos].isdigit():
                        pos += 1
                    tokens.append((line_num, "CONSTANT", line[start:pos]))
                    continue

                # assignment arrow
                if line[pos : pos + 2] == "=>":
                    tokens.append((line_num, "ASSIGN_ARROW", "=>"))
                    pos += 2
                    continue

                # comma
                if c == ",":
                    tokens.append((line_num, "COMMA", ","))
                    pos += 1
                    continue

                # opcode
                if c.isalpha():
                    start = pos
                    while pos < len(line) and line[pos].isalpha():
                        pos += 1
                    tokens.append((line_num, "OPCODE", line[start:pos]))
                    continue

                # ignore invalid chars
                pos += 1
    return tokens


# Function To Read The Tokens Line By Line
def group_by_line(tokens):
    groups = {}
    for t in tokens:
        groups.setdefault(t[0], []).append(t)
    return groups


def parse_line(tokens, line_num):
    instr = [t for t in tokens if t[1] != "COMMENT"]
    if not instr:
        return None, []
    i, errs = 0, []
    if instr[i][1] != "OPCODE":
        return None, [f"Error detected on line {line_num}: Expected OPCODE"]
    op = instr[i][2]
    i += 1
    if op not in VALID_OPCODES:
        return None, [f"Error on line {line_num}: Invalid opcode '{op}'"]

    if op == "nop":
        return ("nop",), (
            []
            if i == len(instr)
            else errs + [f"Error detected on line {line_num}: Extra after nop"]
        )
    if op == "output":
        if i >= len(instr) or instr[i][1] != "REGISTER":
            return None, [f"Error detected on line {line_num}: output needs register."]
        return ("output", instr[i][2]), [] if i + 1 == len(instr) else errs

    if op == "loadI":
        if (
            i + 2 >= len(instr)
            or instr[i][1] != "CONSTANT"
            or instr[i + 1][1] != "ASSIGN_ARROW"
            or instr[i + 2][1] != "REGISTER"
            or i + 3 != len(instr)
        ):
            return None, [
                f"Error detected on line {line_num}: loadI constant => register expected."
            ]
        return ("loadI", instr[i][2], instr[i + 2][2]), []

    if op in {"load", "store"}:
        if (
            i + 2 >= len(instr)
            or instr[i][1] != "REGISTER"
            or instr[i + 1][1] != "ASSIGN_ARROW"
            or instr[i + 2][1] != "REGISTER"
        ):
            return None, [f"Error detected on line {line_num}: {op} rX => rY expected."]
        return (op, instr[i][2], instr[i + 2][2]), []

    # arithmetic operations
    if op in {"add", "sub", "mult", "lshift", "rshift"}:
        if (
            i + 4 >= len(instr)
            or any(
                instr[j][1] != expected
                for j, expected in zip(
                    range(i, i + 4), ["REGISTER", "COMMA", "REGISTER", "ASSIGN_ARROW"]
                )
            )
            or instr[i + 4][1] != "REGISTER"
        ):
            return None, [
                f"Error detected on line {line_num}: {op} rA, rB => rC expected."
            ]
        return (op, instr[i][2], instr[i + 2][2], instr[i + 4][2]), []

    return None, [f"Error detected on line {line_num}: Unhandled opcode"]


def main():
    if not sys.argv[1:] or "-h" in sys.argv[1:]:
        print(
            "Usage: 411fe [flag] [file]\n  -h help\n  -s scan\n  -p parse\n  -r print IR\nDefault: -p"
        )
        return

    args = sys.argv[1:]
    if "-r" in args:
        mode = "-r"
        i = args.index("-r")
    elif "-p" in args:
        mode = "-p"
        i = args.index("-p")
    elif "-s" in args:
        mode = "-s"
        i = args.index("-s")
    else:
        mode = "-p"  # default
        i = -1  # no flag

    # Get file path
    if i != -1 and i + 1 < len(args):
        path = args[i + 1]
    elif len(args) > (i + 1 if i != -1 else 0):
        path = args[0] if i == -1 else args[i + 1]  # fallback
    else:
        print("Error: No input file provided.")
        return

    if not os.path.exists(path):
        print("Error: File not found.")
        return

    tokens = scan_file(path)
    if mode == "-s":
        for ln, typ, lex in tokens:
            # keep comments
            if typ != "COMMENT" or True:
                print(f"{ln} {typ} {lex}")
        return

    groups = group_by_line(tokens)
    irs, errors = [], []
    for ln in sorted(groups):
        ir, errs = parse_line(groups[ln], ln)
        errors.extend(errs)
        if ir:
            irs.append((ln, ir))

    if errors:
        for e in errors:
            print(e)
        with open("error.log", "w") as f:
            f.write("\n".join(errors) + "\n")
    elif mode == "-p":
        print("VALID ILOC PROGRAM")

    if mode == "-r" and not errors:
        for ln, ir in irs:
            op = ir[0]
            if op == "nop":
                print(f"Line {ln}: nop")
            elif op == "output":
                print(f"Line {ln}: output — {ir[1]}")
            elif op == "loadI":
                print(f"Line {ln}: loadI — op1: {ir[1]} — dest: {ir[2]}")
            elif op in {"load", "store"}:
                print(
                    f"Line {ln}: {op} — {'src' if op=='load' else ir[1]}: {ir[1]} — {'dest' if op=='load' else ''} {ir[2]}".strip()
                )
                (
                    print(f"Line {ln}: {op} — {ir[1]} => {ir[2]}")
                    if op == "store"
                    else None
                )
            else:  # arithmetic
                print(f"Line {ln}: {op} — {ir[1]}, {ir[2]} => {ir[3]}")


if __name__ == "__main__":
    main()
