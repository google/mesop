load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

filegroup(
    name = "examples_files",
    srcs = glob(["*.py"]),
)

py_library(
    name = "examples",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop",
    ],
)
