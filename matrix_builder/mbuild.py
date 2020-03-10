"""Build a C++ project using a build matrix."""

# pylint: disable=bad-continuation

import argparse
import os
import shutil
import subprocess
import sys

PROCESSOR_COUNT = str(len(os.sched_getaffinity(0)))


def main():
    """Main entry point for the script."""
    arguments = parse_command_line()
    compilers = {
        #"gcc6": {"CC": "gcc-6", "CXX": "g++-6"},
        #"gcc7": {"CC": "gcc-7", "CXX": "g++-7"},
        "gcc8": {"CC": "gcc-8", "CXX": "g++-8"},
        #"gcc9": {"CC": "gcc-9", "CXX": "g++-9"},
    }
    for compiler in compilers:
        for build_type in ["Release", "Debug"]:
            clean_build_directory(arguments.build_directory)
            run_conan(arguments.source_directory, arguments.build_directory)
            run_cmake(
                arguments.source_directory,
                arguments.build_directory,
                compilers[compiler],
                build_type,
            )
            run_build(arguments.build_directory)
            run_unit_tests(arguments.build_directory)


def parse_command_line() -> argparse.Namespace:
    """
    Build an argument parser, and parse the command line.

    :returns: The parsed command line arguments. File paths are sanitized before returning.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Use a build matrix to build a C++ project with multiple tools, and in "
        "multiple configurations.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="0.1",
        help="Print the application version and exit.",
    )
    parser.add_argument(
        "--source-directory",
        default=os.getcwd(),
        type=str,
        help="The directory which contains the project to build. This directory must already "
        "exist.",
    )
    parser.add_argument(
        "--build-directory",
        default=os.path.abspath(os.path.join(os.getcwd(), "..", "build")),
        type=str,
        help="The directory in which to run builds. If the directory does not exist, it will be "
        "created. WARNING: This directory, and all of its contents, are erased before each build!",
    )
    arguments = parser.parse_args()
    arguments.source_directory = os.path.abspath(
        os.path.expanduser(arguments.source_directory)
    )
    arguments.build_directory = os.path.abspath(
        os.path.expanduser(arguments.build_directory)
    )
    if not os.path.isdir(arguments.source_directory):
        sys.exit(f"{arguments.source_directory} does not exist.")
    if os.path.exists(arguments.build_directory) and os.path.isfile(
        arguments.build_directory
    ):
        sys.exit(f"{arguments.build_directory} exists but is not a directory.")
    return arguments


def clean_build_directory(build_directory) -> None:
    """Wipe the build directory, and create it anew."""
    if os.path.exists(build_directory):
        shutil.rmtree(build_directory)
    os.mkdir(build_directory)


def run_conan(source_directory: str, build_directory: str) -> None:
    """Run Conan to install dependencies."""
    subprocess.run(
        ["conan", "install", source_directory],
        cwd=build_directory,
        check=True,
    )


def run_cmake(
    source_directory: str, build_directory: str, compiler: dict, build_type: str
) -> None:
    """
    Run CMake to generate a build system.

    This is tricky. Using ``env`` to set the C and C++ compilers does not work. ``subprocess.run()``
    needs to run the command in a native shell, which requires using a string for the command,
    instead of a list of strings.
    """
    subprocess.run(
        f"CC={compiler['CC']} CXX={compiler['CXX']} "
        f"cmake -D CMAKE_BUILD_TYPE={build_type} {source_directory}",
        cwd=build_directory,
        check=True,
        shell=True,
    )


def run_build(build_directory: str) -> None:
    """Run the build tool to build the software."""
    subprocess.run(
        ["cmake", "--build", ".", "--parallel", PROCESSOR_COUNT],
        cwd=build_directory,
        check=True,
    )


def run_unit_tests(build_directory) -> None:
    """Run the unit tests."""
    subprocess.run(
        ["ctest", "--parallel", PROCESSOR_COUNT, "--label-regex", "unit"],
        cwd=build_directory,
        check=True,
    )


if __name__ == "__main__":
    main()
