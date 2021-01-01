"""Batch build a CMake-based project."""

import os.path
import subprocess

build_types = ["Release", "Debug"]
compilers = ["g++-6", "g++-7", "g++-8", "g++-9", "clang++-8", "clang++-9"]
build_root = os.path.expanduser("~/repositories/igloo/build")
source_root = os.path.expanduser("~/repositories/igloo/igloo")

for compiler in compilers:
    for build_type in build_types:
        build_directory = os.path.join(build_root, f"cmatrix_{compiler}_{build_type}")
        subprocess.run(
            [
                "ctest",
                "--build-and-test",
                source_root,
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
