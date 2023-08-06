=============
Commitizen
=============

    Python 3 command line utility to standardize commit messages and bump version


.. image:: https://img.shields.io/travis/Woile/commitizen.svg?style=flat-square
    :alt: Travis
    :target: https://travis-ci.org/Woile/commitizen

.. image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
    :alt: Conventional Commits
    :target: https://conventionalcommits.org

.. image:: https://img.shields.io/pypi/v/commitizen.svg?style=flat-square
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/commitizen/

..  image:: https://img.shields.io/pypi/pyversions/commitizen.svg?style=flat-square
    :alt: Supported versions
    :target: https://pypi.org/project/commitizen/

.. image:: https://img.shields.io/codecov/c/github/Woile/commitizen.svg?style=flat-square
    :alt: Codecov
    :target: https://codecov.io/gh/Woile/commitizen

.. image:: docs/images/demo.gif
    :alt: Example running commitizen

.. contents::
    :depth: 2


About
==========

Interactive tool to commit based on established rules (like conventional commits).

It comes with some defaults commit styles,
like conventional commits and jira and it's easily extendable.

It's useful for teams, because it is possible to standardize the commiting style.

Also includes an automatic version bump system based on semver.


Installation
=============

::

    pip install -U commitizen

::

    poetry add commitizen --dev


**Global installation**

::

    sudo pip3 install -U commitizen

Features
========

- Prompt your commit rules to the user
- Display information about your commit rules (schema, example, info)
- Auto **bump** version based on semver using your rules (currently there is only support for conventionalcommits)
- Future: New documentation
- Future: Autochangelog


Commit rules
============

This client tool prompts the user with information about the commit.

Based on `conventional commits <https://conventionalcommits.org/>`_

This is an example of how the git messages history would look like:

::

    BREAKING CHANGE: command send has been removed
    fix: minor typos in code
    feat: new command update
    docs: improved commitizens tab in readme
    feat(cz): jira smart commits
    refactor(cli): renamed all to ls command
    feat: info command for angular
    docs(README): added badges
    docs(README): added about, installation, creating, etc
    feat(config): new loads from ~/.cz and working project .cz .cz.cfg and setup.cfg

Commitizens
===========

These are the available commiting styles by default:

* cz_conventional_commits: `conventional commits <https://conventionalcommits.org/>`_
* cz_jira: `jira smart commits <https://confluence.atlassian.com/fisheye/using-smart-commits-298976812.html>`_


The installed ones can be checked with:

::

    cz ls



Commiting
=========

Run in your terminal

::

    cz commit

or the shortcut

::

    cz c


Usage
=====

::

    $ cz --help
    usage: cz [-h] [--debug] [-n NAME] [--version]
            {ls,commit,c,example,info,schema,bump} ...

    Commitizen is a cli tool to generate conventional commits.
    For more information about the topic go to https://conventionalcommits.org/

    optional arguments:
    -h, --help            show this help message and exit
    --debug               use debug mode
    -n NAME, --name NAME  use the given commitizen
    --version             get the version of the installed commitizen

    commands:
    {ls,commit,c,example,info,schema,bump}
        ls                  show available commitizens
        commit (c)          create new commit
        example             show commit example
        info                show information about the cz
        schema              show commit schema
        bump                bump semantic version based on the git log


Configuration
==============

**New!**: Support for ``pyproject.toml``

In your ``pyproject.toml`` you can add an entry like this:

::

    [tool.commitizen]
    name = cz_conventional_commits
    version = "0.1.0"
    files = [
        "src/__version__.py",
        "pyproject.toml"
    ]


Also, you can create in your project folder a file called
:code:`.cz`, :code:`.cz.cfg` or in your :code:`setup.cfg`
or if you want to configure the global default in your user's home
folder a :code:`.cz` file with the following information:

::

    [commitizen]
    name = cz_conventional_commits
    version = 0.1.0
    files = [
        "src/__version__.py",
        "pyproject.toml"
        ]

The extra tab at the end (``]``) is required.

Creating a commiter
========================

Create a file starting with :code:`cz_` for example :code:`cz_jira.py`.
This prefix is used to detect the plugin. Same method `flask uses <http://flask.pocoo.org/docs/0.12/extensiondev/>`_

Inherit from :code:`BaseCommitizen` and you must define :code:`questions`
and :code:`message`. The others are optionals.


.. code-block:: python

    from commitizen import BaseCommitizen

    class JiraCz(BaseCommitizen):

        def questions(self):
            """Questions regarding the commit message.

            :rtype: list
            """
            questions = [
                {
                    'type': 'input',
                    'name': 'title',
                    'message': 'Commit title'
                },
                {
                    'type': 'input',
                    'name': 'issue',
                    'message': 'Jira Issue number:'
                },
            ]
            return questions

        def message(self, answers):
            """Generate the message with the given answers.

            :type answers: dict
            :rtype: string
            """
            return '{0} (#{1})'.format(answers['title'], answers['issue'])

        def example(self):
            """Provide an example to help understand the style (OPTIONAL)
            Used by cz example.

            :rtype: string
            """
            return 'Problem with user (#321)'

        def schema(self):
            """Show the schema used (OPTIONAL)

            :rtype: string
            """
            return '<title> (<issue>)'

        def info(self):
            """Explanation of the commit rules. (OPTIONAL)
            :rtype: string
            """
            return 'We use this because is useful'


    discover_this = JiraCz  # used by the plugin system


The next file required is :code:`setup.py` modified from flask version

.. code-block:: python

    from distutils.core import setup

    setup(
        name='JiraCommitizen',
        version='0.1.0',
        py_modules=['cz_jira'],
        license='MIT',
        long_description='this is a long description',
        install_requires=['commitizen']
    )

So at the end we would have

::

    .
    ├── cz_jira.py
    └── setup.py

And that's it, you can install it without uploading to pypi by simply doing
:code:`pip install .` If you feel like it should be part of the repo, create a
PR.

Python 2 support
=================

There's no longer support for python 2. Nor planned suppport.

Contributing
============

Feel free to create a PR.

1. Clone the repo.
2. Add your modifications
3. Create a virtualenv
4. Run :code:`pytest -s --cov-report term-missing --cov=commitizen tests/`
