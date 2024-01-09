load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_LIBCST", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

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
        "//mesop/components/badge:py",
        "//mesop/components/box:py",
        "//mesop/components/button:py",
        "//mesop/components/checkbox:py",
        "//mesop/components/divider:py",
        "//mesop/components/icon:py",
        "//mesop/components/input:py",
        "//mesop/components/markdown:py",
        "//mesop/components/progress_bar:py",
        "//mesop/components/progress_spinner:py",
        "//mesop/components/radio:py",
        "//mesop/components/select:py",
        "//mesop/components/slide_toggle:py",
        "//mesop/components/slider:py",
        "//mesop/components/text:py",
        "//mesop/components/tooltip:py",
        "//mesop/protos:ui_py_pb2",
    ],
)

py_test(
    name = "component_configs_test",
    srcs = ["component_configs_test.py"],
    deps = [
        ":editor",
        "//mesop/components",
        "//mesop/components/button:py",
    ] + THIRD_PARTY_PY_PYTEST,
)

py_test(
    name = "editor_codemod_test",
    srcs = ["editor_codemod_test.py"],
    deps = [
        ":editor",
    ] + THIRD_PARTY_PY_LIBCST,
)
