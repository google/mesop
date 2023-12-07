"""
Bazel macro for defining an Optic component, which includes the Python, client-side (TS) and proto targets.
"""

load("@my_deps//:requirements.bzl", "requirement")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "jspb_proto_library", "ng_module", "py_proto_library")

def optic_component(name, ng_deps = [], py_deps = []):
    """
    Defines a new Optic component which includes Python, client-side (TypeScript) and proto targets.

    Args:
        name (str): The name of the component. Must be in snake_case.
        ng_deps (list, optional): List of Angular dependencies for the component. Defaults to an empty list.
        py_deps (list, optional): List of Python dependencies for the component. Defaults to an empty list.
    """
    jspb_proto_target = name + "_jspb_proto"
    py_proto_target = name + "_py_pb2"
    ng_module(
        name = "ng",
        srcs = native.glob([
            "*.ts",
        ]),
        assets = native.glob([
            "*.ng.html",
        ]),
        deps = [
            ":" + jspb_proto_target,
            "//protos:ui_jspb_proto",
            "//web/src/services",
            "@npm//@angular/compiler",
            "@npm//@angular/material",
        ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS + ng_deps,
    )

    native.py_library(
        name = "py",
        srcs = native.glob(["*.py"]),
        deps = [
            ":" + py_proto_target,
            requirement("pydantic"),
            "//optic/component_helpers",
            "//optic/events",
            "//protos:ui_py_pb2",
        ] + py_deps,
    )

    proto_library(
        name = "proto",
        srcs = native.glob(["*.proto"]),
    )

    py_proto_library(
        name = py_proto_target,
        deps = [":proto"],
    )

    jspb_proto_library(
        name = jspb_proto_target,
        deps = [":proto"],
    )
