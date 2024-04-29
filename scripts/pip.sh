#!/bin/bash
#
# Run this script from the workspace root:
#
# To run in clean mode (default):
# $ source ./scripts/pip.sh
#
# To run in dirty mode:
# $ MESOP_DIRTY=true source ./scripts/pip.sh
#
# Note: using source ensures the current directory & env are set
# to the current shell which makes completing the smoke test
# described in publishing.md more convenient.

# Check if MESOP_DIRTY environment variable is set to true
if [ "$MESOP_DIRTY" = "true" ]; then
  echo "Running in dirty mode. (not running bazel clean)"
  rm -rf /tmp/mesoprelease-test
else
  echo "Running in clean mode."
  rm -rf /tmp/mesoprelease-test && bazel clean --expunge
fi

virtualenv --python python3 /tmp/mesoprelease-test/venv-test && \
source /tmp/mesoprelease-test/venv-test/bin/activate && \
pip install --upgrade pip && \
pip install -r mesop/pip_package/requirements.txt --no-binary pydantic && \
pip uninstall -y mesop && \
bazel run //mesop/pip_package:build_pip_package -- /tmp/mesoprelease-test/mesop.tar.gz && \
cp -r ./scripts/smoketest_app /tmp/mesoprelease-test && \
cd /tmp/mesoprelease-test/ && \
tar -xzf mesop.tar.gz && \
pip install --upgrade /tmp/mesoprelease-test/mesop*.whl && \
cd smoketest_app && mesop main.py
