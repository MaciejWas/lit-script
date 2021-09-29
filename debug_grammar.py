from lit_script import Interpreter

interpreter = Interpreter()

while True:
    cmd_input = input("lit-script : ")
    if cmd_input.lower() in ["exit", "quit"]:
        exit(0)
    else:
        interpreter.read(cmd_input)