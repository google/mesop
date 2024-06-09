#Workspace for angular material
workspace(
    name = "mesop",
    # managed_directories = {"@npm": ["node_modules"]},
)

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "bazel_gazelle",
    sha256 = "b7387f72efb59f876e4daae42f1d3912d0d45563eac7cb23d1de0b094ab588cf",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.34.0/bazel-gazelle-v0.34.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.34.0/bazel-gazelle-v0.34.0.tar.gz",
    ],
)

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

#####################
# Python
#####################

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

# Use Python 3.10 because of https://github.com/aspect-build/rules_py/issues/159
python_register_toolchains(
    name = "python_3_10",
    python_version = "3.10",
)

load("@python_3_10//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "my_deps",
    python_interpreter_target = interpreter,
    requirements_lock = "//build_defs:requirements_lock.txt",
)

# Load the starlark macro, which will define your dependencies.
load("@my_deps//:requirements.bzl", "install_deps")

# Call it to define repos for your requirements.
install_deps()

http_archive(
    name = "aspect_rules_py",
    sha256 = "50b4b43491cdfc13238c29cb159b7ccacf0a1e54bd27b65ff2d5fac69af4d46f",
    strip_prefix = "rules_py-0.4.0",
    url = "https://github.com/aspect-build/rules_py/releases/download/v0.4.0/rules_py-v0.4.0.tar.gz",
)

# Fetches the rules_py dependencies.
# If you want to have a different version of some dependency,
# you should fetch it *before* calling this.
# Alternatively, you can skip calling this function, so long as you've
# already fetched all the dependencies.
load("@aspect_rules_py//py:repositories.bzl", "rules_py_dependencies")

rules_py_dependencies()

#####################
# Proto
#####################

http_archive(
    name = "bazel_skylib",
    sha256 = "66ffd9315665bfaafc96b52278f57c7e2dd09f5ede279ea6d39b2be471e7e3aa",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.4.2/bazel-skylib-1.4.2.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.4.2/bazel-skylib-1.4.2.tar.gz",
    ],
)

load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")

bazel_skylib_workspace()

# Using an old version of protobuf due to issue with protobuf javascript ERR:
# In file included from external/com_google_protobuf_javascript/generator/protoc-gen-js.cc:33:
# external/com_google_protobuf_javascript/generator/js_generator.h:39:10: fatal error: 'google/protobuf/stubs/logging.h' file not found
# #include <google/protobuf/stubs/logging.h>
http_archive(
    name = "com_google_protobuf",
    sha256 = "22fdaf641b31655d4b2297f9981fa5203b2866f8332d3c6333f6b0107bb320de",
    strip_prefix = "protobuf-21.12",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v21.12.tar.gz"],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

http_archive(
    name = "rules_proto",
    sha256 = "903af49528dc37ad2adbb744b317da520f133bc1cbbecbdd2a6c546c9ead080b",
    strip_prefix = "rules_proto-6.0.0-rc0",
    url = "https://github.com/bazelbuild/rules_proto/releases/download/6.0.0-rc0/rules_proto-6.0.0-rc0.tar.gz",
)

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")

http_archive(
    name = "rules_proto_grpc",
    sha256 = "9ba7299c5eb6ec45b6b9a0ceb9916d0ab96789ac8218269322f0124c0c0d24e2",
    strip_prefix = "rules_proto_grpc-4.5.0",
    urls = ["https://github.com/rules-proto-grpc/rules_proto_grpc/releases/download/4.5.0/rules_proto_grpc-4.5.0.tar.gz"],
)

load("@rules_proto_grpc//:repositories.bzl", "rules_proto_grpc_repos", "rules_proto_grpc_toolchains")

rules_proto_grpc_toolchains()

rules_proto_grpc_repos()

rules_proto_dependencies()

rules_proto_toolchains()

load("@rules_proto_grpc//js:repositories.bzl", rules_proto_grpc_js_repos = "js_repos")

rules_proto_grpc_js_repos()

#####################
# Angular-related
# Based on: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/WORKSPACE
#####################

# Add NodeJS rules
http_archive(
    name = "build_bazel_rules_nodejs",
    sha256 = "709cc0dcb51cf9028dd57c268066e5bc8f03a119ded410a13b5c3925d6e43c48",
    urls = ["https://github.com/bazelbuild/rules_nodejs/releases/download/5.8.4/rules_nodejs-5.8.4.tar.gz"],
)

# Add sass rules
http_archive(
    name = "io_bazel_rules_sass",
    sha256 = "1c89680ca9cbbba33cb9cd462eb328e5782e14c0aa1286b794c71b5333385407",
    strip_prefix = "rules_sass-1.68.0",
    urls = [
        "https://github.com/bazelbuild/rules_sass/archive/1.68.0.zip",
    ],
)

# Add skylib which contains common Bazel utilities. Note that `rules_nodejs` would also
# bring in the skylib repository but with an older version that does not support shorthands
# for declaring Bazel build setting flags.
http_archive(
    name = "bazel_skylib",
    sha256 = "a9c5d3a22461ed7063aa7b088f9c96fa0aaaa8b6984b601f84d705adc47d8a58",
    strip_prefix = "bazel-skylib-8334f938c1574ef6f1f7a38a03550a31df65274e",
    urls = [
        "https://github.com/bazelbuild/bazel-skylib/archive/8334f938c1574ef6f1f7a38a03550a31df65274e.tar.gz",
    ],
)

http_archive(
    name = "rules_pkg",
    sha256 = "d94fd5b08dbdc227d66421cb9513f6c3b94bb3938fad276445a2d562f7df8f35",
    strip_prefix = "rules_pkg-61018b85819d57feb56886316e76e8ed8a4ce378",
    urls = [
        "https://github.com/bazelbuild/rules_pkg/archive/61018b85819d57feb56886316e76e8ed8a4ce378.tar.gz",
    ],
)

load("@rules_pkg//:deps.bzl", "rules_pkg_dependencies")

rules_pkg_dependencies()

bazel_skylib_workspace()

load("@build_bazel_rules_nodejs//:repositories.bzl", "build_bazel_rules_nodejs_dependencies")

build_bazel_rules_nodejs_dependencies()

load("@rules_nodejs//nodejs:repositories.bzl", "nodejs_register_toolchains")

nodejs_register_toolchains(
    name = "nodejs",
    node_repositories = {
        "18.19.1-darwin_arm64": ("node-v18.19.1-darwin-arm64.tar.gz", "node-v18.19.1-darwin-arm64", "0c7249318868877032ed21cc0ed450015ee44b31b9b281955521cd3fc39fbfa3"),
        "18.19.1-darwin_amd64": ("node-v18.19.1-darwin-x64.tar.gz", "node-v18.19.1-darwin-x64", "ab67c52c0d215d6890197c951e1bd479b6140ab630212b96867395e21d813016"),
        "18.19.1-linux_arm64": ("node-v18.19.1-linux-arm64.tar.xz", "node-v18.19.1-linux-arm64", "228ad1eee660fba3f9fd2cccf02f05b8ebccc294d27f22c155d20b233a9d76b3"),
        "18.19.1-linux_ppc64le": ("node-v18.19.1-linux-ppc64le.tar.xz", "node-v18.19.1-linux-ppc64le", "2e5812b8fc00548e2e8ab9daa88ace13974c16b6ba5595a7a50c35f848f7d432"),
        "18.19.1-linux_s390x": ("node-v18.19.1-linux-s390x.tar.xz", "node-v18.19.1-linux-s390x", "15106acf4c9e3aca02416dd89fb5c71af77097042455a73f9caa064c1988ead5"),
        "18.19.1-linux_amd64": ("node-v18.19.1-linux-x64.tar.xz", "node-v18.19.1-linux-x64", "f35f24edd4415cd609a2ebc03be03ed2cfe211d7333d55c752d831754fb849f0"),
        "18.19.1-windows_amd64": ("node-v18.19.1-win-x64.zip", "node-v18.19.1-win-x64", "ff08f8fe253fba9274992d7052e9d9a70141342d7b36ddbd6e84cbe823e312c6"),
    },
    node_version = "18.19.1",
)

load("@build_bazel_rules_nodejs//:index.bzl", "yarn_install")

yarn_install(
    name = "npm",
    # We add the postinstall patches file here so that Yarn will rerun whenever
    # the file is modified.
    data = [
        "//:.yarn/releases/yarn-1.22.17.cjs",
        "//:.yarnrc",
        "//:tools/postinstall/apply-patches.js",
        "//:tools/postinstall/patches/@angular+bazel+16.0.0-next.6.patch",
        "//:tools/postinstall/patches/@bazel+concatjs+5.8.1.patch",
    ],
    # Currently disabled due to:
    #  1. Missing Windows support currently.
    #  2. Incompatibilites with the `ts_library` rule.
    exports_directories_only = False,
    package_json = "//:package.json",
    quiet = False,
    # We prefer to symlink the `node_modules` to only maintain a single install.
    # See https://github.com/angular/dev-infra/pull/446#issuecomment-1059820287 for details.
    symlink_node_modules = True,
    yarn = "//:.yarn/releases/yarn-1.22.17.cjs",
    yarn_lock = "//:yarn.lock",
)

load("@npm//@bazel/protractor:package.bzl", "npm_bazel_protractor_dependencies")

npm_bazel_protractor_dependencies()

# Setup web testing. We need to setup a browser because the web testing rules for TypeScript need
# a reference to a registered browser (ideally that's a hermetic version of a browser)
load("@io_bazel_rules_webtesting//web:repositories.bzl", "web_test_repositories")

web_test_repositories()

# Setup the Sass rule repositories.
load("@io_bazel_rules_sass//:defs.bzl", "sass_repositories")

sass_repositories(
    yarn_script = "//:.yarn/releases/yarn-1.22.17.cjs",
)

# Setup repositories for browsers provided by the shared dev-infra package.
load(
    "@npm//@angular/build-tooling/bazel/browsers:browser_repositories.bzl",
    _dev_infra_browser_repositories = "browser_repositories",
)

_dev_infra_browser_repositories()

load("@build_bazel_rules_nodejs//toolchains/esbuild:esbuild_repositories.bzl", "esbuild_repositories")

esbuild_repositories(
    npm_repository = "npm",
)

#####################
# Mesop
#####################

load("@//:workspace.bzl", "op_workspace")

op_workspace()
