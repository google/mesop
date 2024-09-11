load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "web_component",
    srcs = glob(["*.py"]),
    data = glob([
        "*.js",
        "*.css",
    ]),
    deps = [
        "//mesop",
        "//mesop/examples/web_component/async_action",
        "//mesop/examples/web_component/code_mirror_editor",
        "//mesop/examples/web_component/complex_props",
        "//mesop/examples/web_component/copy_to_clipboard",
        "//mesop/examples/web_component/custom_font_csp_repro",
        "//mesop/examples/web_component/firebase_auth",
        "//mesop/examples/web_component/hotkeys",
        "//mesop/examples/web_component/markedjs",
        "//mesop/examples/web_component/plotly",
        "//mesop/examples/web_component/quickstart",
        "//mesop/examples/web_component/shared_js_module",
        "//mesop/examples/web_component/slot",
        "//mesop/examples/web_component/svg_icon",
    ],
)
