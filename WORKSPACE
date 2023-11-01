load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Update the SHA and VERSION to the lastest version available here:
# https://github.com/bazelbuild/rules_python/releases.
http_archive(
    name = "rules_python",
    sha256 = "9d04041ac92a0985e344235f5d946f71ac543f1b1565f2cdbc9a2aaee8adf55b",
    strip_prefix = "rules_python-0.26.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.26.0/rules_python-0.26.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

py_repositories()

python_register_toolchains(
    name = "python_3_11",
    python_version = "3.11",
)

load("@python_3_11//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "my_deps",
    python_interpreter_target = interpreter,
    requirements_lock = "//optic:requirements_lock.txt",
)

# Load the starlark macro, which will define your dependencies.
load("@my_deps//:requirements.bzl", "install_deps")

# Call it to define repos for your requirements.
install_deps()
