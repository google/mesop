load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

filegroup(
    name = "examples_files",
    srcs = glob(["**/*.py"]),
)

py_library(
    name = "examples",
    srcs = glob(["*.py"]),
    deps = [
        # REF(//scripts/scaffold_component.py):insert_component_e2e_import
        "//mesop",
        "//mesop/components/slider/e2e",
        "//mesop/components/select/e2e",
        "//mesop/components/radio/e2e",
        "//mesop/components/slide_toggle/e2e",
        "//mesop/components/progress_spinner/e2e",
        "//mesop/components/progress_bar/e2e",
        "//mesop/components/icon/e2e",
        "//mesop/components/divider/e2e",
        "//mesop/components/badge/e2e",
        "//mesop/components/tooltip/e2e",
        "//mesop/components/input/e2e",
        "//mesop/components/markdown/e2e",
        "//mesop/components/text_input/e2e",
        "//mesop/components/box/e2e",
        "//mesop/components/checkbox/e2e",
        "//mesop/components/text/e2e",
        "//mesop/examples/docs",
        "//mesop/examples/shared",
    ],
)
