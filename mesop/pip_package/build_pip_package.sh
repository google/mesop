#!/bin/sh
# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

usage() {
  cat <<EOF
usage: build_pip_package OUTPUT_DIR

Build mesop Pip packages and store the resulting wheel files
into OUTPUT (a directory or "tar.gz" path).

Arguments:
  OUTPUT: A path ending in ".tar.gz" for the output archive, or else a
    path to an existing directory into which to store the wheel files
    directly.
EOF
}

main() {
  if [ $# -ne 1 ]; then
    usage 2>&1
    return 1
  fi
  output="$1"

  if [ -z "${RUNFILES+set}" ]; then
    RUNFILES="$(CDPATH="" cd -- "$0.runfiles" && pwd)"
  fi

  if [ "$(uname)" = "Darwin" ]; then
    workdir="$(mktemp -d -t mesop-pip)"
  else
    workdir="$(mktemp -d -p /tmp -t mesop-pip.XXXXXXXXXX)"
  fi
  original_wd="${PWD}"
  cd "${workdir}" || return 2

  cleanup() {
    rm -r "${workdir}"
  }
  trap cleanup EXIT

  log_file="${workdir}/log"
  build >"${log_file}" 2>&1
  exit_code=$?
  if [ "${exit_code}" -ne 0 ]; then
    cat "${log_file}" >&2
  fi
  return "${exit_code}"
}

build() (
  set -eux
  if [ "$(uname)" = "Darwin" ]; then
    sedi="sed -i ''"
  else
    sedi="sed -i"
  fi

  command -v virtualenv >/dev/null
  [ -d "${RUNFILES}" ]

  cp -LR "${RUNFILES}/mesop/mesop" .
  cp -LR "${RUNFILES}/rules_python" .
  mv -f "mesop/pip_package/LICENSE" .
  mv -f "mesop/pip_package/MANIFEST.in" .
  mv -f "mesop/pip_package/README.md" .
  mv -f "mesop/pip_package/requirements.txt" .
  mv -f "mesop/pip_package/setup.cfg" .
  mv -f "mesop/pip_package/setup.py" .
  mv -f "mesop/pip_package/version.py" .
  rm -rf "mesop/pip_package"

  rm -f mesop/mesop  # bazel py_binary sh wrapper
  chmod -x LICENSE  # bazel symlinks confuse cp
  find . -name __init__.py -exec chmod -x {} +  # which goes for all genfiles


  chmod -R u+w,go+r .

  virtualenv -q -p python3 venv
  export VIRTUAL_ENV=venv
  export PATH="${PWD}/venv/bin:${PATH}"
  unset PYTHON_HOME

  # Require wheel for bdist_wheel command, and setuptools 36.2.0+ so that
  # env markers are handled (https://github.com/pypa/setuptools/pull/1081)
  export PYTHONWARNINGS=ignore:DEPRECATION  # suppress Python 2.7 deprecation spam
  pip install -qU wheel 'setuptools>=36.2.0'

  # Overrides file timestamps in the zip archive to make the build
  # reproducible. (Date is mostly arbitrary, but must be past 1980 to be
  # representable in a zip archive.)
  export SOURCE_DATE_EPOCH=1577836800  # 2020-01-01T00:00:00Z

  python setup.py bdist_wheel --python-tag py3 >/dev/null

  cd "${original_wd}"  # Bazel gives "${output}" as a relative path >_>
  case "${output}" in
    *.tar.gz)
      mkdir -p "$(dirname "${output}")"
      "${RUNFILES}/mesop/mesop/pip_package/deterministic_tar_gz" \
          "${output}" "${workdir}"/dist/*.whl
      ;;
    *)
      if ! [ -d "${output}" ]; then
        printf >&2 'fatal: no such output directory: %s\n' "${output}"
        return 1
      fi
      mv "${workdir}"/dist/*.whl "${output}"
      ;;
  esac
)

main "$@"
