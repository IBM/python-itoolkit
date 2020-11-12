# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## 1.8.0 (2020-11-12)


### Features

* Allow non-string iData values ([6055cf3](https://github.com/IBM/python-itoolkit/commit/6055cf3071f4839f4733a46038f8e90ecc3d3b19))
* Allow transport objects to be closed ([030b930](https://github.com/IBM/python-itoolkit/commit/030b930e0a27242dafc4ac9ca026d27b3524f517)), closes [#64](https://github.com/IBM/python-itoolkit/issues/64)
* Convert DirectTransport to use ctypes ([0758a39](https://github.com/IBM/python-itoolkit/commit/0758a3911dd6c2afe5c61755826f4fab69137af9))
* Make iData value optional (dft to empty str) ([bbab36d](https://github.com/IBM/python-itoolkit/commit/bbab36dfa87eb1181f404622d5a991def807991b))
* Move transport call() functionality to _call() ([f00770c](https://github.com/IBM/python-itoolkit/commit/f00770c7209ae214cc84358e5996aeb1015d81fe))


### Bug Fixes

* Call parent constructor in SSH transport ([8e06c58](https://github.com/IBM/python-itoolkit/commit/8e06c58940acd4c74c23c4bf3458f94529328e29))
* Correct flake8 errors in _direct.py ([a2dbe22](https://github.com/IBM/python-itoolkit/commit/a2dbe22518b69d13252fcd0399591616ce756e46))
* Quote CL cmd in iCmd5250 for shell escaping ([#50](https://github.com/IBM/python-itoolkit/issues/50)) ([9d98acd](https://github.com/IBM/python-itoolkit/commit/9d98acddc140f3792f50e89d92ee0a2a15fc0fc9)), closes [#49](https://github.com/IBM/python-itoolkit/issues/49)
* Update coverage for Python 3.8 support ([5a59916](https://github.com/IBM/python-itoolkit/commit/5a5991620eaabb3d6578d9bf804d0f9ddc9b01e8))
