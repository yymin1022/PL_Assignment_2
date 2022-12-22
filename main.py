import sys

code = ""
functions = []

isMainFunction = False

def main(argv):
    global code

    scriptFile = open(argv[1], "r")

    for curLine in scriptFile.readlines():
        code += curLine.strip()

    scriptFile.close()

    getFunctions()

    if not isMainFunction:
        print("No Starting Function")


def getFunctions():
    global code, functions, isMainFunction

    functions = code.split("}")
    functions.pop(-1)

    for i in range(len(functions)):
        function = functions[i]
        functionAnalyze = function.split("{")

        functionAnalyze[0] = functionAnalyze[0].rstrip()
        functionAnalyze[1] = functionAnalyze[1].rstrip()

        if functionAnalyze[0] == "main":
            isMainFunction = True

        functions[i] = [functionAnalyze[0], functionAnalyze[1]]

    print(functions)


if __name__ == "__main__":
    main(sys.argv)
