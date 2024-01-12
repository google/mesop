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
        "//mesop/protos:ui_py_pb2",
        "//mesop/runtime",
    ] + THIRD_PARTY_PY_LIBCST,
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

py_test(
    name = "editor_codemod_test",
    srcs = ["editor_codemod_test.py"],
    data = [":testdata_files"],
    deps = [
        ":editor",
        "//mesop/utils",
    ] + THIRD_PARTY_PY_LIBCST,
)

filegroup(
    name = "testdata_files",
    srcs = glob(["testdata/**/*.py"]),
)
