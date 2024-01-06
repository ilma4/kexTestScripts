#!/usr/bin/env python3
import os
import sys

mock_results = "./kex/temp/"
master_results = "./clean-kex/temp/"
logName = "kex.log"

def getCoverage(s : str) -> str:
    return s[s.find("Coverage of"):] 



for f in os.listdir(mock_results):
    print(f"processing {f}")
    mock_content = open(mock_results + f + f"/{logName}").read()
    mock_res = getCoverage(mock_content)

    master_content = open(master_results + f + f"/{logName}").read()
    master_res = getCoverage(master_content)
    if mock_res != master_res:
        print(f"{f} has differences!")
        print("Mock results:")
        print("\n".join(mock_res.splitlines()[:6]))
        print('----------')
        print("Master results:")
        print("\n".join(master_res.splitlines()[:6]))
        print()
    print()