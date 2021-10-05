from lit_script import Interpreter

interpreter = Interpreter()

while True:
    cmd_input = input("lit-script : ")
    if cmd_input.lower() in ["exit", "quit"]:
        exit(0)
    elif cmd_input.lower().strip() == "{":

        cmd_input = ""
        while True:
            inside = input("lit-script   ")
            if inside.lower().strip() == "}":
                interpreter.read(cmd_input)
                break
            else:
                cmd_input += inside + "\n"

    else:
        interpreter.read(cmd_input)
