load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")
load("//builddefs:protos.bzl", "py_proto_library")
load("//tools:defaults.bzl", "ng_module")

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
        ":text_ts_proto",
        "//web/src/services",
        "@npm//@angular/compiler",
        "@npm//@angular/material",
    ],
)

py_library(
    name = "py",
    srcs = glob(["*.py"]),
    deps = [
        ":text_py_proto",
        "//optic/component_helpers",
        "//protos:ui_py_proto",
    ],
)

proto_library(
    name = "text_proto",
    srcs = ["text.proto"],
)

py_proto_library(
    name = "text_py_proto",
    srcs = ["text.proto"],
)

js_proto_library(
    name = "text_ts_proto",
    protos = [":text_proto"],
)
