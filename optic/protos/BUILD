load("//build_defs:defaults.bzl", "jspb_proto_library", "proto_library", "py_proto_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

proto_library(
    name = "ui_proto",
    srcs = ["ui.proto"],
)

py_proto_library(
    name = "ui_py_pb2",
    deps = [":ui_proto"],
)

jspb_proto_library(
    name = "ui_jspb_proto",
    deps = [":ui_proto"],
)
