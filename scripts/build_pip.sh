rm -rf dist/ && \
bazel run //mesop/pip_package:build_pip_package -- $(pwd)/dist/mesop.tar.gz && \
cd dist && \
tar -xzf mesop.tar.gz && \
rm mesop.tar.gz
