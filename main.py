import sys

code = ""
functions = []

mainIdx = -1

def main(argv):
    global code, mainIdx

    scriptFile = open(argv[1], "r")

    for curLine in scriptFile.readlines():
        code += curLine.strip()

    scriptFile.close()

    getFunctions()

    if mainIdx < 0:
        print("No Starting Function")
        return

    for idx in range(len(functions)):
        checkFunctions(idx)

    runFunction(mainIdx)


def getFunctions():
    global code, functions, mainIdx

    functions = code.split("}")
    functions.pop(-1)

    for i in range(len(functions)):
        function = functions[i]
        functionAnalyze = function.split("{")

        functionAnalyze[0] = functionAnalyze[0].rstrip()
        functionAnalyze[1] = functionAnalyze[1].rstrip()

        if functionAnalyze[0] == "main":
            mainIdx = i

        functions[i] = [functionAnalyze[0], functionAnalyze[1], []]


def checkFunctions(idx):
    global functions
    curFunctionBody = functions[idx][1].split(";")

    for statement in curFunctionBody:
        if statement.split(" ")[0] == "variable":
            defVariables(statement, idx)

    functions[idx][1] = curFunctionBody


def defVariables(statement, idx):
    for word in statement.split(" "):
        if word != "variable":
            if word[-1] == ",":
                word = word[:-1]
            functions[idx][2].append(word)


def runFunction(idx):
    global functions
    curFunction = functions[idx][1]

    for stmt in curFunction:
        if stmt != "":
            runStatement(stmt)


def runStatement(stmt):
    global functions

    stmt = stmt.split(" ")

    if stmt[0] == "variable":
        pass
    elif stmt[0] == "call":
        print(f"Called {stmt[1]}")

        for idx in range(len(functions)):
            if functions[idx][0] == stmt[1]:
                runFunction(idx)
    elif stmt[0] == "print_ari":
        print("Print Stack")
    else:
        print("Print Variable")


if __name__ == "__main__":
    main(sys.argv)
