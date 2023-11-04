# Requires manually installing protoc and protoc-gen-mypy
# protoc: `brew install protobuf` v25
# protoc-gen-mypy: `pip3 install mypy-protobuf` v3.5.0
protoc --plugin=/Users/will/mambaforge/bin/protoc-gen-mypy -I=protos --python_out=protos --mypy_out=protos  protos/ui.proto