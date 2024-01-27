load("@rules_proto//proto:defs.bzl", "proto_lang_toolchain")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

package_group(
    name = "mesop_internal",
    packages = [
        "-//mesop/examples/...",
        "//...",
    ],
)

# Mesop Example code:
# This is a placeholder where there's an actual allowlist in
# the downstream sync.
package_group(
    name = "mesop_examples",
    packages = [
        "//...",
    ],
)

# Public API:
# This is a placeholder where there's an actual allowlist in
# the downstream sync.
package_group(
    name = "mesop_users",
    packages = [
        "//...",
    ],
)

package(default_visibility = ["//visibility:private"])

# Borrowed from: https://github.com/bazelbuild/rules_python/blob/a1169f1bda00cdf607d0fa173a93d72145d343bc/python/private/proto/BUILD.bazel#L38
proto_lang_toolchain(
    name = "python_toolchain",
    command_line = "--python_out=%s",
    plugin = "//mesop/protos/bin:protoc_gen_mypy",
    plugin_format_flag = "--plugin=protoc-gen-mypy=%s",
    progress_message = "Generating Python proto_library %{label}",
    runtime = "@com_google_protobuf//:protobuf_python",
    # NOTE: This isn't *actually* public. It's an implicit dependency of py_proto_library,
    # so must be public so user usages of the rule can reference it.
    visibility = ["//visibility:public"],
)

compile_pip_requirements(
    name = "pip_requirements",
    requirements_in = ":requirements.txt",
    requirements_txt = ":requirements_lock.txt",
)
