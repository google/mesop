load("//build_defs:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
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
        "//protos:ui_jspb_proto",
        "@npm//@angular/compiler",
    ],
)
