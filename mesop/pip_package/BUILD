# Description:
#  Tools for building the Mesop pip package.
load("//build_defs:defaults.bzl", "py_binary", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

licenses(["notice"])

py_library(
    name = "version",
    srcs = ["version.py"],
    visibility = ["//build_defs:mesop_internal"],
)

sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = [
        "LICENSE",
        "MANIFEST.in",
        "README.md",
        "requirements.txt",
        "setup.cfg",
        "setup.py",
        "version.py",
        ":deterministic_tar_gz",
        "//mesop",  # Main Mesop target
        "//mesop/bin",  # CLI binary
        "//mesop/labs",  # Mesop labs target
    ],
)

py_binary(
    name = "deterministic_tar_gz",
    srcs = ["deterministic_tar_gz.py"],
)
