load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "app_base",
    srcs = glob(["*.py"]),
    data = glob([
        "static/**/*",
    ]),
    deps = [
        "//mesop",
    ],
)
