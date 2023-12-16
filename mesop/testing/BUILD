load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "index",
    srcs = ["index.py"],
    deps = [
        # REF(//scripts/scaffold_component.py):insert_component_e2e_import
        "//mesop/components/form_field/e2e",
        "//mesop/components/input/e2e",
        "//mesop/components/markdown/e2e",
        "//mesop/components/text_input/e2e",
        "//mesop/components/box/e2e",
        "//mesop/components/checkbox/e2e",
        "//mesop/components/text/e2e",
        "//mesop/examples",
    ],
)
