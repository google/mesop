load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "copy_to_clipboard",
    srcs = glob(["*.py"]),
    data = glob(["*.js"]),
    deps = [
        "//mesop",
    ],
)
