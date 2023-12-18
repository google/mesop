load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "mesop",
    srcs = [
        "__init__.py",
        "api.py",
    ],
    deps = [
        # REF(//scripts/scaffold_component.py):insert_component_import
        "//mesop/components/slider:py",
        "//mesop/components/select:py",
        "//mesop/components/radio:py",
        "//mesop/components/slide_toggle:py",
        "//mesop/components/progress_spinner:py",
        "//mesop/components/progress_bar:py",
        "//mesop/components/icon:py",
        "//mesop/components/divider:py",
        "//mesop/components/badge:py",
        "//mesop/components/tooltip:py",
        "//mesop/components/input:py",
        "//mesop/components/markdown:py",
        "//mesop/components/text_input:py",
        "//mesop/components/box:py",
        "//mesop/components",
        "//mesop/components/button:py",
        "//mesop/components/checkbox:py",
        "//mesop/components/text:py",
        "//mesop/events",
        "//mesop/features",
        "//mesop/server",
    ],
)
