load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "nodejs_binary", "py_binary", "py_library", "ts_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "component_specs",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/protos:ui_py_pb2",
    ],
)

py_binary(
    name = "checkbox_spec",
    srcs = glob(["*.py"]),
    main = "checkbox_spec.py",
    deps = [
        # ":component_specs",
        "//mesop/protos:ui_py_pb2",
    ] + THIRD_PARTY_PY_ABSL_PY,
)

ts_library(
    name = "ts_lib",
    srcs = glob(["*.ts"]),
    deps = [
        "@npm//@types/node",
        "@npm//typescript",
    ],
)

nodejs_binary(
    name = "generate_spec",
    data = [":ts_lib"],
    entry_point = "generate_spec.ts",
)
