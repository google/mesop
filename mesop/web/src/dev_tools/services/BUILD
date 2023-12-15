load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "THIRD_PARTY_JS_RXJS", "ng_module")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "services",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//mesop/web/src/utils",
        # REF(//scripts/scaffold_component.py):insert_component_jspb_proto_import
        "//mesop/components/markdown:markdown_jspb_proto",
        "//mesop/components/box:box_jspb_proto",
        "//mesop/components/button:button_jspb_proto",
        "//mesop/components/checkbox:checkbox_jspb_proto",
        "//mesop/components/text:text_jspb_proto",
        "//mesop/components/text_input:text_input_jspb_proto",
        "//mesop/protos:ui_jspb_proto",
    ] + ANGULAR_CORE_DEPS + THIRD_PARTY_JS_RXJS,
)
