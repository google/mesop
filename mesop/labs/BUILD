load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "labs",
    srcs = ["__init__.py"],
    visibility = ["//build_defs:mesop_users"],
    deps = [
        ":labs_impl",
    ],
)

py_library(
    name = "labs_impl",
    srcs = glob(
        ["*.py"],
        exclude = ["__init__.py"],
    ),
    deps = [
        "//mesop",
    ],
)
