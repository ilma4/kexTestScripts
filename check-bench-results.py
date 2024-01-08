#!/usr/bin/env python3
from calendar import c
import os
from re import L
import sys

mockPath = "./kex/temp"
masterPath = "./clean-kex/temp"
logName = "kex.log"

differenceMode = "short"


def getCoverage(text : str) -> str:
    return text[text.find("Coverage of"):] 


def readCoverage(path: str) -> str:
    print(f"Reading {path}")
    if (not os.path.exists(path)):
        print(f"File {path} does not exist!")
        return ""

    content = open(path).read()
    return getCoverage(content)


def displayCoverage(result: str, name: str):
    print(f"{name} results:")
    if (differenceMode == "full"):
        print(result)
    elif (differenceMode == "short"):
        print("\n".join(result.splitlines()[:6]))


def printDiff(mock_res: str, master_res: str):
    if differenceMode == "short":
        print("Mock:")
        print("\n".join(mock_res.splitlines()[:6]))
        print("Master:")
        print("\n".join(master_res.splitlines()[:6]))
    elif differenceMode == "full":
        mock_funcs = mock_res.split("Coverage of")
        master_funcs = master_res.split("Coverage of")
        for i in range(0, len(mock_funcs)):
            if mock_funcs[i] != master_funcs[i]:
                print(f"Function {i} is different!")
                print("Mock:")
                print(mock_funcs[i])
                print("Master:")
                print(master_funcs[i])
            else:
                print(f"Function {i} results are the same!")
            

def compareTest(test: str):
    mock_log_path = os.path.join(mockPath, test, logName)
    mock_log = open(mock_log_path).read()
    mock_res = getCoverage(mock_log)

    master_res = readCoverage(os.path.join(masterPath, test, logName))

    print(f"Comparing {test}...")
    if mock_res != master_res:
        print(f"{test} has differences!")
        if differenceMode == "short":
            print("Mock:")
            print("\n".join(mock_res.splitlines()[:6]))
            print("Master:")
            print("\n".join(master_res.splitlines()[:6]))
        elif differenceMode == "full":
            mock_funcs = mock_res.split("Coverage of")
            master_funcs = master_res.split("Coverage of")
            for i in range(0, len(mock_funcs)):
                if mock_funcs[i] != master_funcs[i]:
                    print(f"Function {i} is different!")
                    print("Mock:")
                    print(mock_funcs[i])
                    print("Master:")
                    print(master_funcs[i])
                else:
                    print(f"Function {i} results are the same!")
    else:
        print(f"{test} is the same!")   
    print(f"MockDescriptors: {countMockDescriptorCreations(mock_log)}")


def countMockDescriptorCreations(log: str) -> int:
    return log.count("Created mock descriptor for")


def countNotFoundMethodForMock(log: str) -> int:
    return log.count("No mock for ")


def check_all():
    for test in os.listdir(mockPath):
        compareTest(test)
        print()


def main():
    global differenceMode
    print("Current directory: ", os.getcwd())
    if len(sys.argv) == 1:
        differenceMode = "short"
        check_all()
        return
    else:
        differenceMode = "full"
        for test in sys.argv[1:]:
            compareTest(test)
        return


if __name__ == "__main__":
    main() 