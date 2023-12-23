load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "component_renderer",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]),
    deps = [
        # REF(//scripts/scaffold_component.py):insert_component_import
        "//mesop/components/slider:ng",
        "//mesop/components/select:ng",
        "//mesop/components/radio:ng",
        "//mesop/components/slide_toggle:ng",
        "//mesop/components/progress_spinner:ng",
        "//mesop/components/progress_bar:ng",
        "//mesop/components/icon:ng",
        "//mesop/components/divider:ng",
        "//mesop/components/badge:ng",
        "//mesop/components/tooltip:ng",
        "//mesop/components/input:ng",
        "//mesop/components/markdown:ng",
        "//mesop/components/box:ng",
        "//mesop/components/box:box_jspb_proto",
        "//mesop/components/button:ng",
        "//mesop/components/checkbox:ng",
        "//mesop/components/text:ng",
        "//mesop/protos:ui_jspb_proto",
    ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)
