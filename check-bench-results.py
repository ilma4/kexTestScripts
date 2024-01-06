#!/usr/bin/env python3
import os
import sys

mock_results = "./kex/temp"
master_results = "./clean-kex/temp"
logName = "kex.log"

def getCoverage(text : str) -> str:
    return text[text.find("Coverage of"):] 


def readCoverage(path: str) -> str:
    print(f"Reading {path}")
    if (not os.path.exists(path)):
        return ""

    content = open(path).read()
    return getCoverage(content)


def compareTest(test: str):
    mock_res = readCoverage(f"{mock_results}/{test}/{logName}")
    master_res = readCoverage(f"{master_results}/{test}/{logName}")

    print(f"Comparing {test}...")
    if mock_res != master_res:
        print(f"{test} has differences!")
        print("Mock results:")
        print("\n".join(mock_res.splitlines()[:6]))
        print('----------')
        print("Master results:")
        print("\n".join(master_res.splitlines()[:6]))
        print()
    else:
        print(f"{test} is the same!")   


def check_all():
    for test in os.listdir(mock_results):
        compareTest(test)
        print()


def main():
    print("Current directory: ", os.getcwd())
    if len(sys.argv) == 1:
        check_all()
        return
    else:
        for test in sys.argv[1:]:
            compareTest(test)
        return

if __name__ == "__main__":
    main() 