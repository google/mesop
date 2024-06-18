load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "editor",
    srcs = glob(
        ["*.py"],
        exclude = ["*_test.py"],
    ),
    deps = [
        "//mesop/components",
        "//mesop/protos:ui_py_pb2",
        "//mesop/runtime",
    ],
)

py_test(
    name = "component_configs_test",
    srcs = ["component_configs_test.py"],
    deps = [
        ":editor",
        "//mesop/components",
        "//mesop/components/box:py",
        "//mesop/components/button:py",
        "//mesop/components/radio:py",
        "//mesop/labs",
    ] + THIRD_PARTY_PY_PYTEST,
)
