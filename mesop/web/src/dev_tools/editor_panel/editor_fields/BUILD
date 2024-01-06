load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "THIRD_PARTY_JS_RXJS", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "editor_fields",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.ng.html",
    ]) + [":editor_fields.css"],
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/component_renderer",
        "//mesop/web/src/dev_tools/component_tree",
        "//mesop/web/src/dev_tools/object_tree",
        "//mesop/web/src/dev_tools/services",
        "//mesop/web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + THIRD_PARTY_JS_RXJS,
)

sass_binary(
    name = "styles",
    src = "editor_fields.scss",
    sourcemap = False,
)
