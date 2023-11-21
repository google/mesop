# Build optic (need to generate protos)
bazel build //optic/cli && \
# Create venv and activate it
bazel run //optic/server:dev_server.venv && \
source .dev_server.venv/bin/activate && \
# Setup py modules for proto dirs
./setup_proto_py_modules.sh && \
# Install pip deps
pip install -r optic/requirements_lock.txt && \
# Run actual typecheck
yarn pyright
