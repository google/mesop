load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "ng_module")

package(
    default_visibility = ["//build_defs:optic_internal"],
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
        # REF(//scripts/gen_component.py):insert_component_import
        "//optic/components/text_input:ng",
        "//optic/components/box:ng",
        "//optic/components/button:ng",
        "//optic/components/checkbox:ng",
        "//optic/components/text:ng",
        "//optic/protos:ui_jspb_proto",
    ] + ANGULAR_CORE_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)
