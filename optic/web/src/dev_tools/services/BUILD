load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "THIRD_PARTY_JS_RXJS", "ng_module")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "services",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//optic/web/src/utils",
        # REF(//scripts/gen_component.py):insert_component_jspb_proto_import
        "//optic/components/box:box_jspb_proto",
        "//optic/components/button:button_jspb_proto",
        "//optic/components/checkbox:checkbox_jspb_proto",
        "//optic/components/text:text_jspb_proto",
        "//optic/components/text_input:text_input_jspb_proto",
        "//optic/protos:ui_jspb_proto",
    ] + ANGULAR_CORE_DEPS + THIRD_PARTY_JS_RXJS,
)
