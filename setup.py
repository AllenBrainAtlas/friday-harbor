# Copyright 2013 Allen Institute for Brain Science
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.




from setuptools import setup, find_packages
setup(
    name = "friday_harbor",
    version = "0.4",
    packages = find_packages(exclude=["test"]),
    install_requires = [ 'numpy', 'scipy', 'h5py', 'requests' ],
    package_data = { '': ['*.py', '*.sh' ] }
)
