# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================

from setuptools import find_packages, setup

# Intentionally do not import "from mesop.pip_package.version"
# because this will drag in other modules through mesop/__init__.py
# incl. third-party packages like Flask which don't exist
# in this script environment.
from version import VERSION


def get_required_packages():
  with open("requirements.txt") as f:
    return f.read().splitlines()


def get_readme():
  with open("README.md") as f:
    return f.read()


REQUIRED_PACKAGES = get_required_packages()

CONSOLE_SCRIPTS = [
  "mesop = mesop.bin.bin:run_main",
]

setup(
  name="mesop",
  version=VERSION,
  description="Build UIs in Python",
  long_description=get_readme(),
  url="https://github.com/google/mesop",
  author="Google Inc.",
  # Contained modules and scripts.
  packages=find_packages(),
  entry_points={
    "console_scripts": CONSOLE_SCRIPTS,
  },
  package_data={
    "mesop": [
      "web/**/*",
    ],
  },
  install_requires=REQUIRED_PACKAGES,
  tests_require=REQUIRED_PACKAGES,
  python_requires=">=3.10",
  # PyPI package information.
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries",
  ],
  license="Apache 2.0",
  keywords="mesop",
)
