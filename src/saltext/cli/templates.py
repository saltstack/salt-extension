# flake8: noqa

PACKAGE_INIT = """\
# pylint: disable=missing-module-docstring
import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
try:
    from .version import __version__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0.not-installed"
    try:
        from importlib.metadata import version, PackageNotFoundError

        try:
            __version__ = version(__name__)
        except PackageNotFoundError:
            # package is not installed
            pass
    except ImportError:
        try:
            from pkg_resources import get_distribution, DistributionNotFound

            try:
                __version__ = get_distribution(__name__).version
            except DistributionNotFound:
                # package is not installed
                pass
        except ImportError:
            # pkg resources isn't even available?!
            pass
"""

LOADERS_TEMPLATE = '''\
"""
Define the required entry-points functions in order for Salt to know
what and from where it should load this extension's loaders
"""
from . import PACKAGE_ROOT  # pylint: disable=unused-import

{% for loader in loaders %}
  {%- set loader_docstring = loader.rstrip("s") %}
  {%- if loader_docstring == "module" %}
      {%- set loader_docstring = "execution" %}
  {%- endif %}
def get_{{ loader }}_dirs():
    """
    Return a list of paths from where salt should load {{ loader.rstrip("s") }} modules
    """
    return [str(PACKAGE_ROOT / "{{ loader.rstrip("s") + "s" }}")]

{% endfor %}
'''

LOADER_TEMPLATE = '''\
{%- set loader_name = loader.rstrip("s") -%}
"""
Salt {{ loader_name }} module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "{{ package_name }}"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The {{ project_name }} {{ loader_name }} module is not implemented yet")
    return __virtualname__
'''

MODULE_LOADER_TEMPLATE = '''\
"""
Salt execution module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "{{ package_name }}"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The {{ project_name }} {{ loader_name }} module is not implemented yet")
    return __virtualname__


def example_function(text):
    """
    This example function should be replaced

    CLI Example:

    .. code-block:: bash

        salt '*' {{ package_name}}.example_function text="foo bar"
    """
    return __salt__["test.echo"](text)
'''

STATE_LOADER_TEMPLATE = '''\
{%- set loader_name = loader.rstrip("s") %}
"""
Salt {{ loader_name }} module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "{{ package_name }}"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The {{ project_name }} {{ loader_name }} module is not implemented yet")

    # Replace this with your own logic
    if "{{package_name}}.example_function" not in __salt__:
        return False, "The '{{package_name}}' execution module is not available"
    return __virtualname__


def exampled(name):
    """
    This example function should be replaced
    """
    ret = {"name": name, "changes": {}, "result": False, "comment": ""}
    value = __salt__["{{package_name}}.example_function"](name)
    if value == name:
        ret["result"] = True
        ret["comment"] = "The '{{package_name}}.example_function' returned: '{}'".format(value)
    return ret
'''

LOADER_MODULE_UNIT_TEST_TEMPLATE = """\
import pytest
import salt.modules.test as testmod
import saltext.{{ package_name }}.{{ loader.rstrip("s") + "s" }}.{{ package_name }}_mod as {{ package_name }}_module


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"test.echo": testmod.echo},
    }
    return {
        {{ package_name }}_module: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    echo_str = "Echoed!"
    assert {{ package_name }}_module.example_function(echo_str) == echo_str
"""

LOADER_STATE_UNIT_TEST_TEMPLATE = """\
import pytest
import salt.modules.test as testmod
import saltext.{{ package_name }}.modules.{{ package_name }}_mod as {{ package_name }}_module
import saltext.{{ package_name }}.{{ loader.rstrip("s") + "s" }}.{{ package_name }}_mod as {{ package_name }}_state


@pytest.fixture
def configure_loader_modules():
    return {
        {{ package_name }}_module: {
            "__salt__": {
                "test.echo": testmod.echo,
            },
        },
        {{ package_name }}_state: {
            "__salt__": {
                "{{ package_name }}.example_function": {{ package_name }}_module.example_function,
            },
        },
    }


def test_replace_this_this_with_something_meaningful():
    echo_str = "Echoed!"
    expected = {
        "name": echo_str,
        "changes": {},
        "result": True,
        "comment": "The '{{package_name}}.example_function' returned: '{}'".format(echo_str),
    }
    assert {{ package_name }}_state.exampled(echo_str) == expected
"""

LOADER_UNIT_TEST_TEMPLATE = """\
{%- set loader_name = loader.rstrip("s") %}
import pytest
import saltext.{{ package_name }}.{{ loader.rstrip("s") + "s" }}.{{ package_name }}_mod as {{ package_name }}_{{ loader_name }}


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        {{ package_name }}_{{ loader_name }}: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in {{ package_name }}_{{ loader_name }}.__salt__
    assert {{ package_name }}_{{ loader_name }}.__salt__["this_does_not_exist.please_replace_it"]() is True
"""

LOADER_MODULE_INTEGRATION_TEST_TEMPLATE = """\
import pytest

pytestmark = [
    pytest.mark.requires_salt_modules("{{ package_name }}.example_function"),
]


def test_replace_this_this_with_something_meaningful(salt_call_cli):
    echo_str = "Echoed!"
    ret = salt_call_cli.run("{{ package_name}}.example_function", echo_str)
    assert ret.exitcode == 0
    assert ret.json
    assert ret.json == echo_str
"""
