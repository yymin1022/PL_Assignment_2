import sys

code = ""
functions = []

def main(argv):
    global code

    scriptFile = open(argv[1], "r")

    for curLine in scriptFile.readlines():
        code += curLine.strip()

    scriptFile.close()

    getFunctions()


def getFunctions():
    global code, functions

    functions = code.split("}")
    functions.pop(-1)

    for i in range(len(functions)):
        function = functions[i]
        functionAnalyze = function.split("{")

        functions[i] = [functionAnalyze[0], functionAnalyze[1]]

    print(functions)


if __name__ == "__main__":
    main(sys.argv)
