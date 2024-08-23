load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "THIRD_PARTY_JS_CODEMIRROR", "ng_module", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "editor_toolbar",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]) + [
        "editor_toolbar.css",
    ],
    deps = [
        "//mesop/protos:ui_jspb_proto",
        "//mesop/web/src/component_renderer",
        "//mesop/web/src/dev_tools",
        "//mesop/web/src/dev_tools/services",
        "//mesop/web/src/error",
        "//mesop/web/src/services",
        "//mesop/web/src/shell",
        "//mesop/web/src/utils",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + ANGULAR_MATERIAL_TS_DEPS + THIRD_PARTY_JS_CODEMIRROR,
)

sass_binary(
    name = "editor_toolbar_styles",
    src = "editor_toolbar.scss",
    sourcemap = False,
)
