load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "jspb_proto_library", "nodejs_binary", "proto_library", "py_binary", "py_library", "py_proto_library", "ts_library")

# Intentionally do not expose this package as this an internal generator.

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
        "//mesop/protos:ui_py_pb2",
    ] + THIRD_PARTY_PY_ABSL_PY,
)

ts_library(
    name = "ts_lib",
    srcs = glob(["*.ts"]),
    devmode_module = "commonjs",
    deps = [
        ":component_spec_jspb_proto",
        "@npm//@types/node",
        "@npm//typescript",
    ],
)

nodejs_binary(
    name = "generate_spec",
    data = [":ts_lib"],
    entry_point = "generate_spec.ts",
)

proto_library(
    name = "component_spec_proto",
    srcs = ["component_spec.proto"],
)

py_proto_library(
    name = "component_spec_py_pb2",
    deps = [":component_spec_proto"],
)

jspb_proto_library(
    name = "component_spec_jspb_proto",
    deps = [":component_spec_proto"],
)
