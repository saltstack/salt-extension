# salt-extension

> Tool to simplify the creation of a new salt extension.

## The why

`salt-extension` is a Python-based CLI tool for generating a project scaffolding
to easily extend [salt](https://github.com/saltstack/salt/) with exec modules, state modules, and more.

Extensions make life easier in several ways:

- Deployments where proprietary Python modules are developed internally, like at enterprises that want to extend `salt` functionality without modifying `salt` itself, can follow a standard.
- Extensions can develop and release at a faster speed than `salt` itself. No need to wait for a specific major release.
- Developing extensions as separate repos allows for smaller, more isolated test suites that are tailored specifically to the scope of the extension.

This approach to development, of the `salt` ecosystem, could also assist in the powers of [Tiamat](https://gitlab.com/saltstack/pop/tiamat) (resources: [SEP26](https://github.com/saltstack/salt-enhancement-proposals/pull/34) // [tiamat-pip](https://gitlab.com/saltstack/pop/tiamat-pip) source code).

Converting existing module sets into extensions could begin treating `salt` as a more "pluggable"/"extensible" ecosystem, and could make it easier to understand what modules haven’t been contributed to in a long time. It is difficult to maintain so many modules within `salt` that manage and orchestrate an ocean of APIs, operating systems, clouds, etc.

## Quickstart

The best way to use this project is with [pipx][pipx]:

    $ pipx install salt-extension
    $ mkdir my_extension
    $ cd my_extension
    $ create-salt-extension my_extension -l states -l module
    Author: John Example Doe
    Author email: jd@example.com
    Summary: An example Salt Extension Module
    Url: https://example.com/my-saltext
    License (apache, other): apache

Then follow the other output instructions.

If all goes well, you should be able to run:

    $ salt-call --local my_extension.example_function text="it worked!"
    local:
        it worked!

Happy hacking!

[pipx]: https://pypi.org/project/pipx/
