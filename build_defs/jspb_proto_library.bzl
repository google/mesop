load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")

def jspb_proto_library(name, deps):
    """
    Shim for JS proto.

    Args:
        name (str): The name of the rule.
        deps (list): A list of dependencies for the rule.

    Example:
        jspb_proto_library(
            name = "my_proto",
            deps = ["//proto:my_proto"],
        )
    """
    js_proto_library(
        name = name,
        protos = deps,
    )
