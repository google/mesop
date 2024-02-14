load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "sxs",
    srcs = glob(["*.py"]),
    data = [
        ":data",
    ],
    deps = [
        "//mesop",
    ],
)

filegroup(
    name = "data",
    srcs = glob(["data/**/*"]),
)
