load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "custom_component",
    srcs = glob(["*.py"]),
    data = ["custom_component.js"],
    deps = [
        "//mesop",
    ],
)
