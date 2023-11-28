load("//tools:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "services",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        # REF(//scripts/gen_component.py):insert_component_ts_proto_import
        "//optic/components/box:box_ts_proto",
        "//optic/components/button:button_ts_proto",
        "//optic/components/checkbox:checkbox_ts_proto",
        "//optic/components/text:text_ts_proto",
        "//optic/components/text_input:text_input_ts_proto",
        "//protos:ui_ts_proto",
        "@npm//@angular/compiler",
    ],
)
