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
uv pip install --upgrade pip && \
uv pip install -r mesop/pip_package/requirements.txt && \
uv pip install gunicorn && \
bazel run //mesop/pip_package:build_pip_package -- /tmp/mesoprelease-test/mesop.tar.gz && \
cp -r ./scripts/smoketest_app /tmp/mesoprelease-test && \
# Do "-P" so that it follows the physical path so that
# it follows the symlink on MacOs from /tmp to /private/tmp
# Otherwise, gunicorn cannot serve the web component files properly
cd -P /tmp/mesoprelease-test/ && \
tar -xzf mesop.tar.gz && \
uv pip install --upgrade /tmp/mesoprelease-test/mesop*.whl && \
cd smoketest_app;

echo -e "\n\033[1;34m=== Instructions to Run the Smoke Test ===\033[0m"
echo -e "\033[1;33m1. Activate the virtual environment:\033[0m"
echo "   source /tmp/mesoprelease-test/venv-test/bin/activate"
echo -e "\033[1;33m2. Run the Mesop application:\033[0m"
echo "   mesop main.py"
echo -e "\033[1;34m=========================================\033[0m\n"
