#!/usr/bin/env python3
import os
import shutil
import subprocess

outputdir = "./temp"
mockitoPath = "runtime-deps/lib/mockito-core-4.11.0.jar"

def run_test(target):
    target = target.replace("/", ".")
    print(f"Running test: {target}")
    output = target.split('.')[-1]
    print(f"target: {target}")
    print(f"output: {output}")
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
    command = [
        "./kex.py",
        "--classpath", classpath,
        "--target", target,
        "--mode", "concolic",
        "--output", f"{outputdir}/{output}"
    ]

    shutil.rmtree(f"{outputdir}/{output}", ignore_errors=True)
    subprocess.run(command, stdout=subprocess.DEVNULL)


def test_all():
    filename = "./test-targets.txt"
    

    # Cleanup existing output directory
    if os.path.exists(outputdir):
        os.system(f"rm -r {outputdir}")

    # Read test targets from file
    filename = "./test-targets.txt"
    with open(filename, 'r') as file:
        for line in file:
            target = line.strip()
            print(target)
            run_test(target)


def main():
    os.chdir(os.path.dirname(os.path.relpath(__file__)))
    print("Current working directory: " + os.getcwd())

    if len(os.sys.argv) > 1:
        for target in os.sys.argv[1:]:
            run_test(target)
        return

    print("Running all tests")
    test_all()


if __name__ == "__main__":
    main() 