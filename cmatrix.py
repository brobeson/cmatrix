"""Batch build a CMake-based project."""

import argparse
import os.path
import subprocess


def main():
    arguments = parse_command_line()
    build_types = ["Release", "Debug"]
    compilers = ["g++-6", "g++-7", "g++-8", "g++-9", "clang++-8", "clang++-9"]

    for compiler in compilers:
        for build_type in build_types:
            # TODO Let the user specify the build directory in the .cmatrix file.
            build_directory = os.path.join(
                arguments.build_directory, f"cmatrix_{compiler}_{build_type}"
            )
            subprocess.run(
                [
                    "ctest",
                    "--build-and-test",
                    arguments.source_directory,
                    build_directory,
                    "--build-generator",
                    "Ninja",
                    "--build-options",
                    "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=on",
                    f"-DCMAKE_CXX_COMPILER:FILEPATH=/usr/bin/{compiler}",
                    f"-DCMAKE_BUILD_TYPE={build_type}",
                    "--test-command",
                    "ctest",
                ],
                check=True,
            )


def parse_command_line() -> argparse.Namespace:
    """
    Parse the command line arguments.

    :return: The command line arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Build a CMake based project with multiple tools and configurations."
    )
    parser.add_argument(
        "source_directory", help="The path to the root of the source tree."
    )
    parser.add_argument(
        "build_directory",
        help="The path to the root of the build tree. Each build will be in a subdirectory of this"
        " directory.",
    )
    arguments = parser.parse_args()
    arguments.source_directory = os.path.abspath(
        os.path.expanduser(arguments.source_directory)
    )
    arguments.build_directory = os.path.abspath(
        os.path.expanduser(arguments.build_directory)
    )
    return arguments


if __name__ == "__main__":
    main()
