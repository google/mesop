# Build optic (need to generate protos)
bazel build //optic/cli && \
# Create venv and activate it
bazel run //optic/cli:cli.venv && \
source .cli.venv/bin/activate && \
# Setup py modules for proto dirs
./scripts/setup_proto_py_modules.sh && \
# Install pip deps
pip install -r build_defs/requirements_lock.txt && \
# Run actual typecheck
yarn pyright
