load("@rules_python//python:defs.bzl", "py_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//builddefs:protos.bzl", "py_proto_library")

package(
    default_visibility = ["//visibility:public"],
)

proto_library(
    name = "ui_proto",
    srcs = ["ui.proto"],
)

py_proto_library(
    name = "ui_py_proto",
    srcs = ["ui.proto"],
)
