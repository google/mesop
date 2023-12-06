load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

py_library(
    name = "optic",
    srcs = [
        "__init__.py",
        "api.py",
    ],
    deps = [
        # REF(//scripts/gen_component.py):insert_component_import
        "//optic/components/text_input:py",
        "//optic/components/box:py",
        "//optic/components",
        "//optic/components/button:py",
        "//optic/components/checkbox:py",
        "//optic/components/text:py",
        "//optic/event_handler",
        "//optic/events",
        "//optic/features",
        "//optic/server",
    ],
)
