import sys

code = ""
functions = []

def main(argv):
    global code

    scriptFile = open(argv[1], "r")

    for curLine in scriptFile.readlines():
        code += curLine.strip()

    scriptFile.close()

    getFunction()


def getFunction():
    global code, functions

    functions = code.split("}")

    for function in functions:
        print(function)


if __name__ == "__main__":
    main(sys.argv)
