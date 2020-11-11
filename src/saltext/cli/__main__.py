import datetime
import os
import pathlib
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

import click
from click_params import PUBLIC_URL
from click_params import SLUG
from jinja2 import Template
from saltext.cli import __version__
from saltext.cli import PACKAGE_ROOT
from saltext.cli.templates import LOADER_TEMPLATE
from saltext.cli.templates import LOADER_TEST_TEMPLATE
from saltext.cli.templates import LOADERS_TEMPLATE
from saltext.cli.templates import PACKAGE_INIT

LICENSES: Dict[str, str] = {
    "apache": "License :: OSI Approved :: Apache Software License",
}

SALT_LOADERS = (
    "auth",
    "beacons",
    "cache",
    "cloud",
    "engines",
    "executor",
    "grain",
    "log_handlers",
    "matchers",
    "metaproxy",
    "module",
    "netapi",
    "output",
    "pillar",
    "proxy",
    "queue",
    "render",
    "returner",
    "roster",
    "runner",
    "serializers",
    "states",
    "thorium",
    "tokens",
    "top",
    "wheel",
    # sdb related
    "sdb",
    "pkgdb",
    "pkgfiles",
    # ssh wrapper
    "wrapper",
)


@click.command()
@click.version_option(version=__version__)
@click.help_option("-h", "--help")
@click.option("-A", "--author", help="Author name", type=str, prompt=True)
@click.option("-E", "--author-email", help="Author Email", type=str, prompt=True)
@click.option("-S", "--summary", help="Project summary", type=str, prompt=True)
@click.option("-U", "--url", help="Project URL", type=PUBLIC_URL, prompt=True)
@click.option("--source-url", help="Project Source URL", type=PUBLIC_URL)
@click.option("--tracker-url", help="Project Tracker URL", type=PUBLIC_URL)
@click.option("--docs-url", help="Project Documentation URL", type=PUBLIC_URL)
@click.option("--package-name", help="Project Package name 'saltex.<package-name>'", type=str)
@click.option(
    "-F",
    "--force-overwrite",
    help="Force overwrites",
    is_flag=True,
    default=False,
    expose_value=True,
)
@click.option(
    "-V", "--salt-version", help="The minimum Salt version to target", default="3001", type=str
)
@click.option(
    "-l",
    "--loader",
    help="Which loaders should the project support",
    type=click.Choice(SALT_LOADERS),
    multiple=True,
)
@click.option(
    "-L",
    "--license",
    help="Project License",
    type=click.Choice(sorted(LICENSES) + ["other"]),
    prompt=True,
)
@click.option(
    "--dest",
    help="The path where to create the new project. Defaults to current directory",
    type=click.Path(
        file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True
    ),
    default=os.getcwd(),
)
@click.argument("project-name", type=SLUG)
def main(
    project_name: str,
    author: str,
    author_email: str,
    summary: str,
    url: PUBLIC_URL,
    source_url: Optional[PUBLIC_URL],
    tracker_url: Optional[PUBLIC_URL],
    docs_url: Optional[PUBLIC_URL],
    package_name: Optional[str],
    license: str,
    loader: Tuple[str],
    dest: str,
    salt_version: str,
    force_overwrite: bool,
):
    destdir: pathlib.Path = pathlib.Path(dest)

    templating_context: Dict[str, Any] = {
        "project_name": project_name,
        "author": author,
        "author_email": author_email,
        "summary": summary,
        "url": url,
        "salt_version": salt_version,
        "copyright_year": datetime.datetime.today().year,
    }

    if not package_name:
        package_name = project_name.replace(" ", "_").replace("-", "_")

    templating_context["package_name"] = package_name

    if not source_url or not tracker_url and "github.com" in url:
        if not source_url:
            source_url = url
        if not tracker_url:
            tracker_url = "{}/issues".format(url.rstrip("/"))
    elif not tracker_url and source_url and "github.com" in source_url:
        tracker_url = "{}/issues".format(source_url.rstrip("/"))

    templating_context.update(
        {
            "source_url": source_url,
            "tracker_url": tracker_url,
        }
    )
    if license == "other":
        click.secho(
            "You can choose your license at https://choosealicense.com and then match "
            "it with the python license classifiers at https://pypi.org/classifiers",
            bold=True,
            fg="bright_yellow",
        )
        click.secho(
            "Make sure you update the 'license' field and also the classifiers on "
            "the generated 'setup.cfg'.",
            bold=True,
            fg="bright_yellow",
        )
    elif license:
        license_name: str = LICENSES[license]
        license_classifier: str = license_name.split(" :: ")[-1]
        templating_context["license"] = license_name
        templating_context["license_classifier"] = license_classifier

    templating_context["loaders"] = loader

    if not destdir.is_dir():
        destdir.mkdir(0o755)

    project_template_path = PACKAGE_ROOT / "project"
    for src in sorted(project_template_path.rglob("*")):
        dst_parts = []
        templating_context["loader"] = loader
        for part in src.relative_to(project_template_path).parts:
            if part.endswith(".j2"):
                dst_parts.append(part[:-3])
                continue
            dst_parts.append(part)
        dst = destdir.joinpath(*dst_parts)
        if src.is_dir():
            if dst.exists():
                continue
            dst.mkdir(src.stat().st_mode, exist_ok=True)
            continue
        if dst.exists() and force_overwrite is False:
            click.secho(
                "Not overwriting '{}'. New name will be '{}'.".format(
                    dst.relative_to(dest), dst.relative_to(dest).with_suffix(".new")
                ),
                fg="bright_red",
            )
            dst = dst.with_suffix(".new")
        contents = src.read_text()
        if src.name.endswith(".j2"):
            contents = Template(contents).render(**templating_context)
        dst.write_text(contents)

    loaders_package_path = destdir / "src" / "saltext" / package_name
    loaders_package_path.mkdir(0o755, parents=True)
    loaders_package_path.joinpath("__init__.py").write_text(
        Template(PACKAGE_INIT).render(**templating_context)
    )
    loaders_package_path.joinpath("loader.py").write_text(
        Template(LOADERS_TEMPLATE).render(**templating_context)
    )
    loaders_unit_tests_path = destdir / "tests" / "unit"
    for loader_name in loader:
        templating_context["loader"] = loader_name
        loader_dir = loaders_package_path / (loader_name.rstrip("s") + "s")
        loader_dir.mkdir(0o755)
        loader_dir_init = loader_dir / "__init__.py"
        if not loader_dir_init.exists():
            loader_dir_init.write_text("")
        loader_module_contents = Template(LOADER_TEMPLATE).render(**templating_context)
        loader_dir_module = loader_dir / f"{package_name}_mod.py"
        if loader_dir_module.exists() and force_overwrite is False:
            loader_dir_module = loader_dir_module.with_suffix(".new")
        loader_dir_module.write_text(loader_module_contents)

        loader_unit_tests_dir = loaders_unit_tests_path / (loader_name.rstrip("s") + "s")
        loader_unit_tests_dir.mkdir(0o755, exist_ok=True)
        loader_unit_tests_dir_init = loader_unit_tests_dir / "__init__.py"
        if not loader_unit_tests_dir_init.exists():
            loader_unit_tests_dir_init.write_text("")
        loader_unit_test_contents = Template(LOADER_TEST_TEMPLATE).render(**templating_context)
        loader_unit_test_module = loader_unit_tests_dir / f"test_{package_name}.py"
        if loader_unit_test_module.exists() and not force_overwrite:
            loader_unit_test_module = loader_unit_test_module.with_suffix(".new")
        loader_unit_test_module.write_text(loader_unit_test_contents)

    click.secho("Bare ones project is created. Start Hacking!", fg="bright_green", bold=True)


if __name__ == "__main__":
    main()
