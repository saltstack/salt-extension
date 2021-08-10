# salt-extension
Tool to simplify the creation of a new salt extension

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
