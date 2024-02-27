package(default_visibility = ["//visibility:public"])

exports_files([
    "terser_config.json",
    "esbuild.config-tmpl.mjs",
])

# Make source files available for distribution via pkg_npm
filegroup(
    name = "files",
    srcs = glob(["*"]),
)
