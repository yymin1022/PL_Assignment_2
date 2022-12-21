import sys

def main(argv):
    scriptFile = open(argv[1], "r")

    inputString = ""
    for curLine in scriptFile.readlines():
        inputString += curLine.strip()

    scriptFile.close()


if __name__ == "__main__":
    main(sys.argv)
