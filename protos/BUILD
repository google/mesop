load("@rules_proto//proto:defs.bzl", "proto_library")
load("//builddefs:defs.bzl", "jspb_proto_library")
load("//builddefs:protos.bzl", "py_proto_library")

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

jspb_proto_library(
    name = "ui_jspb_proto",
    deps = [":ui_proto"],
)
