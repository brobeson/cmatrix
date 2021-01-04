# Using CMatrix

## Installing CMatrix

Clone this repository:

```bash
git clone https://github.com/brobeson/cmatrix.git
```

## Running CMatrix

Use Python 3 to run [*cmatrix.py*](/cmatrix.py).
I use `python3` as the Python 3 command throughout the documentation.
The command might be different on your system.

When you run CMatrix, you must provide the paths to your source tree and where you want the software built.

```text
python3 cmatrix.py /path/to/source /path/to/build
```

For each build matrix element, CMatrix creates a subdirectory in your build directory.
Here is an example to illustrate.
Assume two compilers, gcc and clang, and two build configurations, Release and Debug.
The root build directory is *~/project/build*.
CMatrix will create this directory structure:

```text
~/project/build/cmatrix_gcc_Release/
~/project/build/cmatrix_gcc_Debug/
~/project/build/cmatrix_clang_Release/
~/project/build/cmatrix_clang_Debug/
```

For the latest command line options, run `python3 cmatrix.py --help`.

CMatrix prints each build matrix element with one of the following status icons:

| Icon | Meaning |
|:---|:---|
| :hammer: | The build is running. |
| :white_check_mark: | The build succeeded. |
| :x: | The build failed. |

Example output is:

```text
:white_check_mark: gcc Release
:x: gcc Debug
:white_check_mark: clang Release
:hammer: clang Debug
```

A build's final status is determined by the exit code returned by CMake.
If the exit code is 0, the build succeeded.
The build failed for any other exit code.

Build output is written to *cmatrix.log* in the matrix element's build directory.
Continuing our example, the build output is in these files:

```text
~/project/build/cmatrix_gcc_Release/cmatrix.log
~/project/build/cmatrix_gcc_Debug/cmatrix.log
~/project/build/cmatrix_clang_Release/cmatrix.log
~/project/build/cmatrix_clang_Debug/cmatrix.log
```

> **Warning**
>
> Some build steps may produce warnings or errors, but still return 0 as the exit code.
> One example is running Cppcheck via `CMAKE_CXX_CPPCHECK`.
> Developers should double check the build log for this type of false negative.

## Configuring CMatrix

CMatrix reads configuration options from two configuration files.
The first file is *~/.cmatrix* on Linux and *%USERPROFILE%\\.cmatrix* on Windows.
The second file is *.cmatrix* in the project's source tree.
Options in the second file take precedence over the first file.
Command line options take precedences over both files.

[Configuring CMatrix](configuring_cmatrix.md) contains complete details about the configuration files.
