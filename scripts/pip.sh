#!/bin/bash

# Initialize the dirty flag as false
dirty=false

# Parse command-line options
while getopts "d" opt; do
  case $opt in
    d) dirty=true ;;
    \?) echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
  esac
done

# Now you can use the $dirty variable to conditionally run commands
if [ "$dirty" = true ]; then
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
cd smoketest_app && mesop --path main.py
