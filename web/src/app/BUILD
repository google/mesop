load("//build_defs:defaults.bzl", "ANGULAR_CDK_DEPS", "ANGULAR_CORE_DEPS", "ANGULAR_MATERIAL_DEPS", "JS_STATIC_FILES", "esbuild_config", "ng_module", "npm_sass_library", "sass_binary")

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
        "//protos:ui_jspb_proto",
        "//web/src/component_renderer",
        "//web/src/dev_tools",
        "//web/src/error",
        "//web/src/services",
    ] + ANGULAR_CORE_DEPS,
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

npm_sass_library(
    name = "material_sass_deps",
    deps = ANGULAR_CDK_DEPS + ANGULAR_MATERIAL_DEPS,
)

sass_binary(
    name = "styles",
    src = "styles.scss",
    include_paths = ["external/npm/node_modules"],
    sourcemap = False,
    deps = [":material_sass_deps"],
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
