#!/usr/bin/env python3
from calendar import c
import os
from re import L
import sys
from logUtils import *


firstDir = 'temp'
secondDir = 'temp'
logName = "kex.log"

def mockPath():
    return os.path.join("./kex", firstDir)
def masterPath():
    return os.path.join("./clean-kex", secondDir)

# mockPath = "./kex"
# masterPath = "./clean-kex"

differenceMode = "short"


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
            

def compareTest(test: str) -> ((str, str, str, str), (str, str, str, str)):
    mock_log_path = os.path.join(mockPath(), test, logName)
    mock_log = readFile(mock_log_path) 
    mock_res = getCoverage(mock_log)

    master_res = getCoverage(readFile(os.path.join(masterPath(), test, logName)))

    print(f"Comparing {test}...")
    if differenceMode == "short":
        mock_res = "\n".join(mock_res.splitlines()[:6])
        master_res = "\n".join(master_res.splitlines()[:6])

    if mock_res != master_res:
        print(f"{test} has differences!")
        if differenceMode == "short":
            print("Mock:")
            print(mock_res)
            print("Master:")
            print(master_res)
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

    if differenceMode == "short":
        return (parseCoverage(mock_res), parseCoverage(master_res)) 
    elif differenceMode == "full":
        return "", ""


def check_all():
    coverages = []
    for test in os.listdir(mockPath()):
        mock_cov, master_cov = compareTest(test)
        coverages.append(mock_cov + master_cov)
        print()
    
    if differenceMode == "short":
        print("Coverage results:")
        coverages = '\n'.join(map(lambda x: ' '.join(x), coverages))
        print(coverages)


def main():
    global differenceMode, firstDir, secondDir 
    print("Current directory: ", os.getcwd())
    it = iter(sys.argv)
    targets = list[str]()
    for arg in it:
        if arg == '--dir' or arg == '-bothDir':
            firstDir = next(it)
            secondDir = firstDir
        elif arg == '--firstDir':
            firstDir = next(it)
        elif arg == '--secondDir':
            secondDir = next(it)
        else:
            targets.append(arg)
        

    if len(targets) == 1:
        differenceMode = "short"
        check_all()
        return
    else:
        differenceMode = "full"
        for test in targets[1:]:
            compareTest(test)
        return


if __name__ == "__main__":
    main() 