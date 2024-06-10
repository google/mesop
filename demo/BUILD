load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "demo",
    srcs = glob(["*.py"]),
    data = [":screenshots"],
    deps = [
        "//mesop",
        "//mesop/labs",
    ],
)

# Make source files available for distribution via pkg_npm
filegroup(
    name = "screenshots",
    srcs = glob(["screenshots/*"]),
)
