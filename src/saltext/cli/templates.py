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
from . import PACKAGE_ROOT
{% for loader in loaders %}
  {%- set loader_docstring = loader.rstrip("s") %}
  {%- if loader_docstring == "module" %}
      {%- set loader_docstring = "execution" %}
  {%- endif %}
def get_{{ loader }}_dirs():
    """
    Return a list of paths from where salt should load {{ loader.rstrip("s") }} modules
    """
    return [str(PACKAGE_ROOT / {{ loader.rstrip("s") + "s" }})]

{% endfor %}
'''

LOADER_TEMPLATE = """\
{%- set loader_name = loader.rstrip("s") %}
{%- if loader_name == "module" %}
    {%- set loader_name = "execution" %}
{%- endif %}
import logging

log = logging.getLogger(__name__)

__virtualname__ = "{{ package_name }}"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The {{ project_name }} {{ loader_name }} module is not implemented yet")
    return __virtualname__
"""

LOADER_TEST_TEMPLATE = """\
import pytest
import saltext.{{ package_name }}.{{ loader.rstrip("s") + "s" }}.{{ package_name }}_mod as {{ package_name }}_module

@pytest.fixture
def configure_loader_modules():
    module_globals = {"__salt__": {"this_does_not_exist.please_replace_it": lambda: True}}
    return { {{- package_name -}} _module: module_globals}


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in {{ package_name }}_module.__salt__
    assert {{ package_name }}_module.__salt__["this_does_not_exist.please_replace_it"]() is True
"""
