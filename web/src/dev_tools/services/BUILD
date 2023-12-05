load("//build_defs:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "services",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        # REF(//scripts/gen_component.py):insert_component_jspb_proto_import
        "//optic/components/box:box_jspb_proto",
        "//optic/components/button:button_jspb_proto",
        "//optic/components/checkbox:checkbox_jspb_proto",
        "//optic/components/text:text_jspb_proto",
        "//optic/components/text_input:text_input_jspb_proto",
        "//protos:ui_jspb_proto",
        "@npm//@angular/compiler",
    ],
)
