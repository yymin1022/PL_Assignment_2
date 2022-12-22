import sys

code = ""
functions = []
mainIdx = -1
runtimeStack = []

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

    runtimeStack.append({functions[mainIdx][0]: {}})
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
    functions[idx][1] = functions[idx][1].split(";")


def defVariables(statement, idx):
    for word in statement:
        if word[-1] == ",":
            word = word[:-1]
        functions[idx][2].append(word)

    runtimeStack[-1][functions[idx][0]]["Local Variables"] = functions[idx][2]


def runFunction(idx):
    global functions
    curFunction = functions[idx][1]

    for stmt in curFunction:
        if stmt != "":
            runStatement(idx, stmt)


def runStatement(idx, stmt):
    global functions

    stmt = stmt.split(" ")

    if stmt[0] == "variable":
        defVariables(stmt[1:], idx)
    elif stmt[0] == "call":
        for i in range(len(functions)):
            if functions[i][0] == stmt[1]:
                runtimeStack.append({functions[i][0]: {"Return Address": functions[idx][0]}})
                runFunction(i)
    elif stmt[0] == "print_ari":
        for runtime in reversed(runtimeStack):
            for key in runtime:
                print(f"{key}:")

                for item in reversed(runtime[key]["Local Variables"]):
                    print(f"  Local Variable: {item}")

                if "ReturnAddress" in runtime[key]:
                    print(f"  Return Address: {runtime[key]['Return Address']}")
    else:
        print(f"{functions[idx][0]}:{stmt[0]} => VALUE ")


if __name__ == "__main__":
    main(sys.argv)
