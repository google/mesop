load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

filegroup(
    name = "examples_files",
    srcs = glob(["**/*.py"]),
)

py_library(
    name = "examples",
    srcs = glob(["*.py"]),
    deps = [
        "//demo",
        # REF(//scripts/scaffold_component.py):insert_component_e2e_import
        "//mesop/components/autocomplete/e2e",
        "//mesop/components/link/e2e",
        "//mesop/components/html/e2e",
        "//mesop/components/uploader/e2e",
        "//mesop/components/embed/e2e",
        "//mesop/components/table/e2e",
        "//mesop/components/sidenav/e2e",
        "//mesop/components/video/e2e",
        "//mesop/components/audio/e2e",
        "//mesop/components/image/e2e",
        "//mesop",
        "//mesop/labs",
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
        "//mesop/components/box/e2e",
        "//mesop/components/checkbox/e2e",
        "//mesop/components/text/e2e",
        "//mesop/examples/web_component",
        "//mesop/examples/docs",
        "//mesop/examples/integrations",
        "//mesop/examples/shared",
        "//mesop/examples/starter_kit",
        "//mesop/examples/testing",
    ],
)
