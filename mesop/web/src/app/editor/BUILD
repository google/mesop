load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "JS_STATIC_FILES", "ng_js_binary", "ng_module", "pkg_web")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

# Need this for downstream sync so these static files
# can be depended on by other packages.
exports_files([
    "favicon.ico",
    "index.html",
])

ng_module(
    name = "main",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//mesop/web/src/editor",
    ] + ANGULAR_CORE_DEPS,
)

ng_js_binary(
    name = "editor_bundle",
    entry_points = [":bundle.ts"],
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

# File group for all static files which are needed to serve the editor version of the app.
filegroup(
    name = "editor_static_files",
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
        ":editor_bundle",
        ":editor_static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for index.html & style to be loaded.
        "mesop/web/src/app",
    ],
    tags = ["manual"],
)
