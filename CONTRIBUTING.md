# How to Contribute

These are a few guidelines that contributors need to follow to keep things easy.

## Getting Started

- Create a branch or fork the repository
- Check out the [Developer Guide](#developer-guide) below for setup instructions
- Add your functionality or fix a bug
- Ensure that your changes pass the tests
- Only refactoring and documentation changes require no new tests.
- Only pull requests with passing tests will be accepted.

## Submitting Changes

- Push your changes to your branch/fork.
- Submit a pull request.

## Additional Resources

- [General GitHub documentation](http://help.github.com/)
- [GitHub pull request documentation](http://help.github.com/send-pull-requests/)

---

## Developer Guide

As a developer, you should be aware of the following:

- Linting and formatting with `ruff` and `pyright`
- Testing with `pytest`
- CI/CD with [GitHub Actions](https://docs.github.com/en/actions/quickstart)

### Code Quality

[Ruff](https://docs.astral.sh/ruff/linter/) is used to lint and format the codebase.

### Rye

[Rye](https://rye-up.com/) is used for virtual environments, dependency management
and packaging. The `rye` setup is located in the `rye` field of `pyproject.toml`.

### Unit Testing

[Pytest](https://docs.pytest.org/en/stable/) is used for unit testing. The tests are
located in the `test` directory.

### Installation and Devtools

Using `rye` as the package manager, you may run the following commands:

```bash
# build virtual environment and install dependencies
rye sync

# lint code
rye run lint

# test code
rye test

# build code
rye build --clean
```

To run an example, you will need to follow the instructions in the
[examples/main.py](./examples/main.py) file, then run the following command:

```bash
yarn demo
```

> **Disclaimer:** This project has been carefully ported from this Node.js [library][namefully-js].
> In fact, 90% of that portability was done with the help of GitHub Copilot + ChatGPT 4o.
> This library is also available in [Dart & Flutter][namefully-dart].

[namefully-js]: https://github.com/ralflorent/namefully
[namefully-dart]: https://github.com/ralflorent/namefully-dart
