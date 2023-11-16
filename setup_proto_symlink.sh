# Needed for VS Code to provide Python type-checking against generated proto stubs.
bazel_bin_path=$(bazel info bazel-bin)
# Clean-up old symlink
rm .dev_server.venv/lib/python3.10/site-packages/protos

touch "${bazel_bin_path}/protos/__init__.py" && \
ln -s "${bazel_bin_path}/protos" .dev_server.venv/lib/python3.10/site-packages/protos && \
touch "${bazel_bin_path}/optic/__init__.py" && \
touch "${bazel_bin_path}/optic/components/__init__.py" &&
find "${bazel_bin_path}/optic/components/" -type d -exec touch {}/__init__.py \;
