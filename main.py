import sys

code = ""
functions = []
mainIdx = -1
runtimeStack = []


def main(argv):
    global code, mainIdx, runtimeStack

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

    runtimeStack.append({functions[mainIdx][0]: {"DL": -1, "RA": ""}})
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

        for j in range(len(functions)):
            if i != j and functions[j][0] == functions[i][0]:
                print(f"Duplicate Declaration of the Identifier or the Function Name : {functions[i][0]}")
                exit(0)


def checkFunctions(idx):
    global functions

    functions[idx][1] = functions[idx][1].split(";")


def defVariables(statement, idx):
    global functions, runtimeStack

    for word in statement:
        if word[-1] == ",":
            word = word[:-1]
        functions[idx][2].append(word)

    runtimeStack[-1][functions[idx][0]]["LV"] = functions[idx][2]


def runFunction(idx):
    global functions

    curFunction = functions[idx][1]

    for stmt in curFunction:
        if stmt != "":
            runStatement(idx, stmt)

    runtimeStack.pop()


def runStatement(idx, stmt):
    global functions, runtimeStack

    stmt = stmt.split(" ")

    if stmt[0] == "variable":
        defVariables(stmt[1:], idx)
    elif stmt[0] == "call":
        curDL = 0
        if runtimeStack[-1][functions[idx][0]]["DL"] >= 0:
            curDL = runtimeStack[-1][functions[idx][0]]["DL"] + len(list(runtimeStack[runtimeStack[-1][functions[idx][0]]['DL']].values())[0]['LV'])

        isFunctionOK = False
        for i in range(len(functions)):
            if functions[i][0] == stmt[1]:
                isFunctionOK = True
                runtimeStack.append({functions[i][0]: {"RA": functions[idx][0], "DL": curDL}})
                runFunction(i)

        if not isFunctionOK:
            print(f"Call to Undefined Function : {stmt[1]}")
            exit(0)
    elif stmt[0] == "print_ari":
        for runtime in reversed(runtimeStack):
            for key in runtime:
                print(f"{key}:")

                for item in reversed(runtime[key]["LV"]):
                    print(f"  Local Variable: {item}")

                if int(runtime[key]["DL"]) >= 0:
                    print(f"  Dynamic Link: {runtime[key]['DL']}")
                    print(f"  Return Address: {runtime[key]['RA']}")
    else:
        varFrom = functions[idx][0]
        varName = stmt[0]
        varLinkCnt = 0
        varLocalOffset = 0

        isVarFound = False
        for runtime in reversed(runtimeStack):
            varLocalOffset = 0
            for func in functions:
                if func[0] == list(runtime.keys())[0]:
                    for var in func[2]:
                        if var == varName:
                            isVarFound = True
                            break
                        varLocalOffset += 1
            if isVarFound:
                break
            varLinkCnt += 1

        if not isVarFound:
            print(f"Call to Undefined Variable : {varName}")
            exit(0)

        print(f"{varFrom}:{varName} => {varLinkCnt}:{varLocalOffset}")


if __name__ == "__main__":
    main(sys.argv)
