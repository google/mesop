load("//build_defs:defaults.bzl", "ANGULAR_CDK_TS_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_SASS_DEPS", "ANGULAR_MATERIAL_TS_DEPS", "JS_STATIC_FILES", "esbuild_config", "ng_module", "sass_external_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "app",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "app.ng.html",
    ],
    deps = [
        "//optic/protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/dev_tools",
        "//web/src/error",
        "//web/src/services",
    ] + ANGULAR_CORE_DEPS + ANGULAR_CDK_TS_DEPS + ANGULAR_MATERIAL_TS_DEPS,
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

sass_external_binary(
    name = "styles",
    src = "styles.scss",
    external_deps = ANGULAR_MATERIAL_SASS_DEPS,
    sourcemap = False,
)

# File group for all static files which are needed to serve the dev-app. These files are
# used in the devserver as runfiles and will be copied into the static web package that can
# be deployed on static hosting services (like firebase).
filegroup(
    name = "static_files",
    srcs = [
        ":index.html",
        ":styles",
    ] + JS_STATIC_FILES,
)
