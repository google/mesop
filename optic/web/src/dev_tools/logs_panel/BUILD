load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "THIRD_PARTY_JS_RXJS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "logs_panel",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":logs_panel.css"],
    deps = [
        "//optic/protos:ui_jspb_proto",
        "//optic/web/src/component_renderer",
        "//optic/web/src/dev_tools/object_tree",
        "//optic/web/src/dev_tools/services",
        "//optic/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + THIRD_PARTY_JS_RXJS,
)

sass_binary(
    name = "styles",
    src = "logs_panel.scss",
    sourcemap = False,
)
