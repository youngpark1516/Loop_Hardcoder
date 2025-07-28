import sys
import os

captured_lines = [] # Lines that are captured https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXZjNnVuNzJrdHZ1MmF0YnppZmx6MDdjZ3NibjZ3cGVlOTByYXZoMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/800iiDTaNNFOwytONV/giphy.gif
last_vars = {} 

def tracer(frame, event, arg): # Overwatch reference ?!?!?!?!?!
    if event != 'line':
        return tracer

    code = frame.f_code
    lineno = frame.f_lineno
    filename = code.co_filename

    # Check line
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            line = f.readlines()[lineno - 1].strip()
    except:
        return tracer

    local_vars = frame.f_locals.copy()

    # Variable assignments
    global last_vars
    for var in local_vars:
        if var.startswith("__"):
            continue
        if var not in last_vars or local_vars[var] != last_vars[var]:
            captured_lines.append(f"{var} = {repr(local_vars[var])}")
    last_vars = local_vars

    # Prints
    if line.startswith("print("):
        try:
            val = eval(line[6:-1], frame.f_globals, frame.f_locals)
        except:
            captured_lines.append(f"Failed line: {line}")

    return tracer

def run_hardcoder(path):
    global captured_lines, last_vars
    captured_lines = []
    last_vars = {}

    sys.settrace(tracer)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(compile(code, path, 'exec'), {"__file__": path})
    finally:
        sys.settrace(None)

    return captured_lines

def output(input_path, lines):
    base_name = os.path.basename(input_path)
    new_dir = "fixed"
    os.makedirs(new_dir, exist_ok=True)
    new_path = os.path.join(new_dir, f"fixed_{base_name}")

    with open(new_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Read README.md again")
        sys.exit(1)

    input_path = sys.argv[1]
    lines = run_hardcoder(input_path)

    print("Expanded code:")
    for line in lines:
        print(line)

    output(input_path, lines)