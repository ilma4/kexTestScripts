import os
import re


def countMockDescriptorCreations(log: str) -> int:
    return log.count("Created mock descriptor for")


def countNotFoundMethodForMock(log: str) -> int:
    return log.count("No mock for ")


def getCoverage(text : str) -> str:
    return text[text.find("Coverage of"):] 


def readFile(path: str) -> str:
    print(f"Reading {path}")
    if (not os.path.exists(path)):
        print(f"File {path} does not exist!")
        return ""

    return open(path).read()

# Instructions, branches, lines, complexity
def parseCoverage(results: str) -> (str, str, str, str):
    coverage = re.findall(r"\d+\.\d\d%", results)
    coverage = list(map(lambda x: x[:-1], coverage))
    if len(coverage) != 4:
        print(f"Error parsing coverage! Expected 4 values! Found: {coverage}")
        return ["0", "0", "0", "0"]
    # return (float(coverage[0][:-1]), float(coverage[1][:-1]), float(coverage[2][:-1]), float(coverage[3][:-1]))
    return coverage
