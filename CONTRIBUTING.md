# Contributing

## Contributing In General

Our project welcomes external contributions. If you have an itch, please feel
free to scratch it.

To contribute code or documentation, please submit a [pull request](https://github.com/IBM/python-itoolkit/pulls).

A good way to familiarize yourself with the codebase and contribution process is
to look for and tackle low-hanging fruit in the [issue tracker](https://github.com/IBM/python-itoolkit/issues).
These will be marked with the [good first issue](https://github.com/IBM/python-itoolkit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) label. You may also want to look at those marked with [help wanted](https://github.com/IBM/python-itoolkit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).

**Note: We appreciate your effort, and want to avoid a situation where a contribution
requires extensive rework (by you or by us), sits in backlog for a long time, or
cannot be accepted at all!**

### Proposing new features

If you would like to implement a new feature, please [raise an issue](https://github.com/IBM/python-itoolkit/issues)
before sending a pull request so the feature can be discussed. This is to avoid
you wasting your valuable time working on a feature that the project developers
are not interested in accepting into the code base.

### Fixing bugs

If you would like to fix a bug, please [raise an issue](https://github.com/IBM/python-itoolkit/issues) before sending a
pull request so it can be tracked.

## Legal

We have tried to make it as easy as possible to make contributions. This
applies to how we handle the legal aspects of contribution. We use the
same approach - the [Developer's Certificate of Origin 1.1 (DCO)](https://github.com/hyperledger/fabric/blob/master/docs/source/DCO1.1.txt) - that the Linux® Kernel [community](https://elinux.org/Developer_Certificate_Of_Origin)
uses to manage code contributions.

We simply ask that when submitting a patch for review, the developer
must include a sign-off statement in the commit message.

Here is an example Signed-off-by line, which indicates that the
submitter accepts the DCO:

```text
Signed-off-by: John Doe <john.doe@example.com>
```

You can include this automatically when you commit a change to your
local git repository using the following command:

```bash
git commit -s
```

## Communication

Please feel free to connect with us on our [Ryver forum](https://ibmioss.ryver.com/index.html#forums/1000128). You can join the Ryver community [here](https://ibmioss.ryver.com/application/signup/members/9tJsXDG7_iSSi1Q).

## Setup

This project follows the standard packaging way:

```bash
# Install requirements
python -m pip install -r requirements.txt

# Build
python setup.py build

# Install
python setup.py install
```

## Testing

This package uses [pytest](https://docs.pytest.org/en/latest/) for its tests.
You can run them like so:

```bash
# Test installed package (python setup.py install)
python -m pytest tests

# Test local changes which haven't been installed
PYTHONPATH=src python -m pytest tests
```

## Coding style guidelines

This project will attempt to follow [PEP 8](https://www.python.org/dev/peps/pep-0008) guidelines. New contributions should enforce PEP-8 style and we welcome any changes (see issue [#19](https://github.com/IBM/python-itoolkit/issues/19) for more details)