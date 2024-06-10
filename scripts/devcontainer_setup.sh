# postCreateCommands for devcontainer.json

# Ensure that the node modules directory is writable.
#
# We're storing node modules on a Docker volume (not to be confused with bind mounts on
# the host OS) for better performance. When this volume gets created, it is owned by
# root.
sudo chown mesop-dev:mesop-dev node_modules

# Update third party python packages needed for Mesop.
bazel run //build_defs:pip_requirements.update

# Virtual Env to use with VS Code.
bazel run //mesop/cli:cli.venv
source .cli.venv/bin/activate

# Allows VS Code to recognize third party dependencies.
pip install -r build_defs/requirements_lock.txt

# Allows VS Code to recognize protos.
./scripts/setup_proto_py_modules.sh

# Precommit support for Git (installs into venv)
pip install pre-commit==3.7.1
pre-commit install

# Install playwright
yarn playwright install
