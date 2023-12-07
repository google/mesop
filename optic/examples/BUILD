load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

filegroup(
    name = "examples_files",
    srcs = glob(["*.py"]),
)

py_library(
    name = "examples",
    srcs = glob(["*.py"]),
    deps = [
        "//optic",
    ],
)
