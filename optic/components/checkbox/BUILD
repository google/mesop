load("//tools:defaults.bzl", "ng_module")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")
load("//builddefs:protos.bzl", "py_proto_library")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "ng",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]),
    deps = [
        ":checkbox_ts_proto",
        "//protos:ui_ts_proto",
        "//web/src/services",
        "@npm//@angular/compiler",
        "@npm//@angular/material",
    ],
)

py_library(
    name = "py",
    srcs = glob(["*.py"]),
    deps = [
        ":checkbox_py_proto",
        "//optic/component_helpers",
        "//protos:ui_py_proto",
    ],
)

proto_library(
    name = "checkbox_proto",
    srcs = ["checkbox.proto"],
)

py_proto_library(
    name = "checkbox_py_proto",
    srcs = ["checkbox.proto"],
)

js_proto_library(
    name = "checkbox_ts_proto",
    protos = [":checkbox_proto"],
)
