#!/usr/bin/env python3
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
        print("Mock results:")
        print("\n".join(mock_res.splitlines()[:6]))
        print('----------')
        print("Master results:")
        print("\n".join(master_res.splitlines()[:6]))
    elif differenceMode == "full":
        mock_funcs = mock_res.split("Coverage of")
        master_funcs = master_res.split("Coverage of")
        for i in range(0, len(mock_funcs)):
            if mock_funcs[i] != master_funcs[i]:
                print(f"Function {i} is different!")
                print("Mock results:")
                print(mock_funcs[i])
                print('----------')
                print("Master results:")
                print(master_funcs[i])
                print()
            else:
                print(f"Function {i} results are the same!")
            

def compareTest(test: str):
    mock_res = readCoverage(f"{mockPath}/{test}/{logName}")
    master_res = readCoverage(f"{masterPath}/{test}/{logName}")

    print(f"Comparing {test}...")
    if mock_res != master_res:
        print(f"{test} has differences!")
        printDiff(mock_res, master_res)
        print()
    else:
        print(f"{test} is the same!")   


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