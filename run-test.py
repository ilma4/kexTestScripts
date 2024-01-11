#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

outputdir = "./temp"
mockitoPath = "runtime-deps/lib/mockito-core-4.11.0.jar"
dryRun = False

def run_test(target: str):
    target = target.replace("/", ".")
    print(f"Running test: {target}")
    className = target.split('.')[-1]
    print(f"target: {target}")
    print(f"className: {className}")
    deps = [ "commons-collections/target/commons-collections4-4.5-SNAPSHOT.jar",
    "commons-collections/target/dependency/error_prone_annotations-2.18.0.jar",
    "commons-collections/target/dependency/junit-jupiter-params-5.9.3.jar",
    "commons-collections/target/dependency/hamcrest-core-1.3.jar",
    "commons-collections/target/dependency/easymock-5.1.0.jar",
    "commons-collections/target/dependency/checker-qual-3.33.0.jar",
    "commons-collections/target/dependency/junit-jupiter-engine-5.9.3.jar",
    "commons-collections/target/dependency/junit-platform-engine-1.9.3.jar",
    "commons-collections/target/dependency/commons-lang3-3.13.0.jar",
    "commons-collections/target/dependency/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar",
    "commons-collections/target/dependency/junit-jupiter-api-5.9.3.jar",
    "commons-collections/target/dependency/commons-codec-1.16.0.jar",
    "commons-collections/target/dependency/junit-platform-commons-1.9.3.jar",
    "commons-collections/target/dependency/apiguardian-api-1.1.2.jar",
    "commons-collections/target/dependency/opentest4j-1.2.0.jar",
    "commons-collections/target/dependency/failureaccess-1.0.1.jar",
    "commons-collections/target/dependency/jsr305-3.0.2.jar",
    "commons-collections/target/dependency/objenesis-3.3.jar",
    "commons-collections/target/dependency/guava-testlib-32.1.2-jre.jar",
    "commons-collections/target/dependency/j2objc-annotations-2.8.jar",
    "commons-collections/target/dependency/hamcrest-2.2.jar",
    "commons-collections/target/dependency/junit-4.13.2.jar",
    "commons-collections/target/dependency/commons-io-2.13.0.jar",
    "commons-collections/target/dependency/guava-32.1.2-jre.jar"
    ]

    if os.path.exists(mockitoPath):
        deps.append(mockitoPath)

    classpath = ":".join(deps)      
    output = os.path.join(outputdir, className)
    print(f"Output directory: {output}")

    command = [
        "./kex.py",
        "--classpath", classpath,
        "--target", target,
        "--mode", "concolic",
        "--output",  output   
    ]

    if dryRun:
        return

    shutil.rmtree(output, ignore_errors=True)
    subprocess.run(command, stdout=subprocess.DEVNULL)


def test_all():
    filename = "./test-targets.txt"
    

    # Read test targets from file
    filename = "./test-targets.txt"
    with open(filename, 'r') as file:
        for line in file:
            target = line.strip()
            print(target)
            run_test(target)


def multiple_mode(targets: list[str]):
    print("Testing both kex and clean-kex")
    os.chdir("./kex")
    single_mode(targets)
    print("Switching to clean-kex")
    os.chdir("../clean-kex")
    single_mode(targets)
    print("All done!")


def single_mode(targets: list[str]):
    print("Current working directory: " + os.getcwd())

    if len(targets) != 0:
        for target in targets:
            run_test(target)
        return

    print("Running all tests")
    test_all()


def main():
    global outputdir 
    global dryRun

    targets = list[str]()
    args = iter(sys.argv[1:])
    for arg in args:
        if arg == "--output":
            outputdir = next(args)
        elif arg == "--dry-run":
            dryRun = True
            print("Dry run mode. No tests will be run and no files will be created or deleted")
        else:
            targets.append(arg)

    print(f"Targets from command line: {targets}")

    if os.listdir().__contains__("kex.py"):
        print(f"Testing only {os.path.basename(os.getcwd())}")
        single_mode(targets=targets)
        return
    elif os.listdir().__contains__("kex") and os.listdir().__contains__("clean-kex"):
        multiple_mode(targets=targets)
        return
    else:
        print("Script must be run from kex directory (contains kex.py) or superdirectory containing both kex and clean-kex (clean-kex must be named that)")
        print("Current working directory: " + os.getcwd())
        print(f"Content of directory: {os.listdir()}")
        return


if __name__ == "__main__":
    main() 