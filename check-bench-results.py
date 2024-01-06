#!/usr/bin/env python3
import os
import sys

mock_results = "./kex/temp/"
master_results = "./clean-kex/temp/"
logName = "kex.log"

def getCoverage(s : str) -> str:
    return s[s.find("Coverage of"):] 


def compareTest(test: str):
    mock_content = open(mock_results + test + f"/{logName}").read()
    mock_res = getCoverage(mock_content)

    master_content = open(master_results + test + f"/{logName}").read()
    master_res = getCoverage(master_content)

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
    if len(sys.argv) == 1:
        check_all()
        return
    else:
        for test in sys.argv[1:]:
            compareTest(test)
        return

if __name__ == "__main__":
    main() 