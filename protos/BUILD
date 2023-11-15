load("@rules_proto//proto:defs.bzl", "proto_library")
load("//builddefs:protos.bzl", "py_proto_library")
load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")

package(
    default_visibility = ["//:optic_internal"],
)

proto_library(
    name = "ui_proto",
    srcs = ["ui.proto"],
)

py_proto_library(
    name = "ui_py_proto",
    srcs = ["ui.proto"],
)

js_proto_library(
    name = "ui_ts_proto",
    protos = [":ui_proto"],
)
