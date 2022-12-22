import sys

code = ""
functions = []
mainIdx = -1
runtimeStack = []


def main(argv):
    global code, mainIdx, runtimeStack

    # Read Script File
    scriptFile = open(argv[1], "r")

    for curLine in scriptFile.readlines():
        code += curLine.strip()

    scriptFile.close()

    # Call Function for Splitting Functions
    getFunctions()

    # Check if Main Function Exist
    if mainIdx < 0:
        print("No Starting Function")
        return

    # Split Each Splitted Functions to Statements
    for idx in range(len(functions)):
        checkFunctions(idx)

    # Add Main Function to Runtime Stack
    runtimeStack.append({functions[mainIdx][0]: {"DL": -1, "RA": ""}})
    runFunction(mainIdx)


# Split Each Functions
def getFunctions():
    global code, functions, mainIdx

    functions = code.split("}")
    functions.pop(-1)

    for i in range(len(functions)):
        function = functions[i]
        functionAnalyze = function.split("{")

        functionAnalyze[0] = functionAnalyze[0].rstrip()
        functionAnalyze[1] = functionAnalyze[1].rstrip()

        # Check if this Function is Main Function
        if functionAnalyze[0] == "main":
            mainIdx = i

        functions[i] = [functionAnalyze[0], functionAnalyze[1], []]

        # Exit Program if Duplicated Function Name
        for j in range(len(functions)):
            if i != j and functions[j][0] == functions[i][0]:
                print(f"Duplicate Declaration of the Function Name : {functions[i][0]}")
                exit(0)



# Split Function Body to Statements
def checkFunctions(idx):
    global functions

    functions[idx][1] = functions[idx][1].split(";")


# Define Variables from variable Statements
def defVariables(statement, idx):
    global functions, runtimeStack

    for word in statement:
        if word[-1] == ",":
            word = word[:-1]

        # Check if Duplicated Name with Other Identifier or Function
        for i in range(len(functions)):
            if word == functions[i][0]:
                print(f"Duplicate Declaration of the Identifier or the Function Name : {word}")
                exit(0)

        # Check if Duplicated NAme with Other Identifier
        isVarOK = True
        for i in functions[idx][2]:
            if i == word:
                print(f"Duplicate Declaration of the Identifier : {word}")

        if isVarOK:
            functions[idx][2].append(word)

    # Add Local Variables to Runtime Stack
    runtimeStack[-1][functions[idx][0]]["LV"] = functions[idx][2]


# Run Each Statements in Function
def runFunction(idx):
    global functions

    curFunction = functions[idx][1]

    for stmt in curFunction:
        if stmt != "":
            runStatement(idx, stmt)

    # If Function Ended, Pop from Runtime Stack
    runtimeStack.pop()


# Run Statement
def runStatement(idx, stmt):
    global functions, runtimeStack

    stmt = stmt.split(" ")

    if stmt[0] == "variable":
        # If variable Keyword, start Defining Variable
        defVariables(stmt[1:], idx)
    elif stmt[0] == "call":
        # If call Keyword, start Calling Function
        # Get Current Dynamic Link and start Add New Function to Runtime Stack
        curDL = 0
        if runtimeStack[-1][functions[idx][0]]["DL"] >= 0:
            curDL = runtimeStack[-1][functions[idx][0]]["DL"] + len(list(runtimeStack[runtimeStack[-1][functions[idx][0]]['DL']].values())[0]['LV'])

        isFunctionOK = False
        for i in range(len(functions)):
            if functions[i][0] == stmt[1]:
                isFunctionOK = True
                runtimeStack.append({functions[i][0]: {"RA": functions[idx][0], "DL": curDL}})
                runFunction(i)

        # Check if Undefined Function is Called
        if not isFunctionOK:
            print(f"Call to Undefined Function : {stmt[1]}")
            exit(0)
    elif stmt[0] == "print_ari":
        # If print_ari Keyword, Print Runtime Stack Content
        for runtime in reversed(runtimeStack):
            for key in runtime:
                print(f"{key}:")

                for item in reversed(runtime[key]["LV"]):
                    print(f"  Local Variable: {item}")

                if int(runtime[key]["DL"]) >= 0:
                    print(f"  Dynamic Link: {runtime[key]['DL']}")
                    print(f"  Return Address: {runtime[key]['RA']}")
    else:
        # If just a Variable Keyword
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

        # Check if Undefined Variable is Called
        if not isVarFound:
            print(f"Call to Undefined Variable : {varName}")
            exit(0)

        print(f"{varFrom}:{varName} => {varLinkCnt}:{varLocalOffset}")


if __name__ == "__main__":
    main(sys.argv)
