load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "ng_js_binary", "ng_module", "pkg_web")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "main",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//web/src/app",
    ] + ANGULAR_CORE_DEPS,
)

ng_js_binary(
    name = "bundles",
    entry_points = [":main.ts"],
    deps = [
        ":main",
    ],
)

# Target that builds a static web package of the dev-app. The web package can be
# deployed on static hosting services (such as firebase).
pkg_web(
    name = "web_package",
    srcs = [
        ":bundles",
        "//web/src/app:static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for index.html & style to be loaded.
        "web/src/app",
    ],
    tags = ["manual"],
)
