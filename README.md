
# Lily-Assitant

Set of scripts, git hooks etc. helping us to stick to the high quality standards imposed on our code, tests, documentation, and the way we work with git

## Installation

Just copy and execute the below snippet while being in the ROOT directory of
your project (where one has direct access to `.git`, `src`, `tests`)

```bash
pip install -e git+https://github.com/cosphere-org/lily-assistant.git#egg=lily-assistant

```

in order to install a particular version of the lily-assistant please use the following:
```bash
pip install -e git+https://github.com/cosphere-org/lily-assistant.git@1.0.0#egg=lily-assistant

```

After the installation of Lily-Assitant one should initialize it (while being in the root of one's project) by running:

```bash
lily_assistant init <name_of_src_dir>

```

Where naturally the `<name_of_src_dir>` should be replaced by the name of the src folder.

The above operation will install newest git hooks (`./.git/hooks` directory) and perform so preliminary checks. Finally at the end it will info you about the necessity of adding `include .lily/lily_assistant.makefile` at the top of your Makefile.

## Lily-Assitant Makefile commands

Lily-Assitant exposes various helpful Makefile commands:
- `make lint` - when executed it will run the linter against the tests and source folders
- `make test tests=<path to test directory / file>` - running selected tests
- `make test_all` - running all tests
- `make inspect_coverage` - loads in Chrome browser the html coverage report allowing one to find all lines that are missing coverage etc.

## IDE and Testing

Lily-Assitant assumes that one uses `py.test` for testing therefore if you're triggering your tests to be run by IDE either point them to `make test_all` or `make test test=<path to test directory / file>` or use directly the command rendered in the `.lily/lily_assistant.makefile`

## Lily-Assitant Commands
Lily-Assitant itself exposes plenty of super helpful commands. One can inspect them by running:

```bash
lily_assistant --help

```

## Required project structure

On each commit attempt Lily-Assitant asserts if the stucture of the project is correct. It probes for the following:

    ├── <project_name>/
    ├── tests/
    ├── .git/
    ├── env.sh
    ├── Makefile
    ├── pytest.ini
    ├── README.md
    ├── requirements.txt
    ├── test-requirements.txt
    └── setup.py

Only projects that are fulfilling this structure will pass initial Lily-Assitant checks.

## Development (Lily-Assitant itself)

If one is interested in contributing to Lily-Assitant, please run the following to install its all dependencies:

```bash
make install

```

It's assumed that as per python standards the above command will be executed while being in some sort of virtualenv.

## Going forward

Notice that even though the current code focuses on the python it could be easily extend and applied to other programming languages like Scala. It would only require to set additional makefile.


## Reference

- Naming convention error codes:
    https://github.com/PyCQA/pep8-naming#plugin-for-flake8

- Docstring convetion error codes:
    http://www.pydocstyle.org/en/2.1.1/error_codes.html

- General error codes:
    http://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
