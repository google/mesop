# Needed for VS Code to provide Python type-checking against generated proto stubs.
# TODO: do not hardcode architecture in "bazel-out" path.
touch bazel-out/darwin_arm64-fastbuild/bin/protos/__init__.py && \
ln -s $(pwd)"/bazel-out/darwin_arm64-fastbuild/bin/protos" .dev_server.venv/lib/python3.10/site-packages/protos