load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "JS_STATIC_FILES", "ng_js_binary_prod", "ng_module", "pkg_web")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ng_module(
    name = "main",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//mesop/web/src/shell",
    ] + ANGULAR_CORE_DEPS,
)

ng_js_binary_prod(
    name = "prod_bundle",
    entry_point = "bundle.ts",
    visibility = ["//build_defs:mesop_users"],
    deps = [
        ":main",
    ],
)

genrule(
    name = "styles",
    srcs = ["//mesop/web/src/app:styles.css"],
    outs = ["styles.css"],
    cmd = "cp $(SRCS) $(@D)/styles.css",
)

genrule(
    name = "sandbox_iframe",
    srcs = ["//mesop/web/src/app:sandbox_iframe.html"],
    outs = ["sandbox_iframe.html"],
    cmd = "cp $(SRCS) $(@D)/sandbox_iframe.html",
)

# File group for all static files which are needed to serve the prod version of the app.
filegroup(
    name = "prod_static_files",
    srcs = [
        ":favicon.ico",
        ":index.html",
        ":sandbox_iframe.html",
        ":styles",
    ] + JS_STATIC_FILES,
    visibility = ["//build_defs:mesop_users"],
)

# Target that builds a static web package of the dev-app. The web package can be
# deployed on static hosting services (such as firebase).
pkg_web(
    name = "web_package",
    srcs = [
        ":prod_bundle",
        ":prod_static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for index.html & style to be loaded.
        "mesop/web/src/app",
    ],
    tags = ["manual"],
)
