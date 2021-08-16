# Release Process

Release process consists of the following:

- Permissions
- Tagging
- Generating tarballs
- Uploading to pypi

## Permissions

Proper permissions on `pypi` need to be granted via a **maintainer** listed:

- https://pypi.org/project/salt-extension/

## Tagging

> This process assumes that you have a fork of the repo set as `origin` and the upstream repo is set as `upstream`.

```bash
# New tag/version
NEW_VERSION='0.23.0' # Modify to release

# All work should be coming from main
git checkout main
git fetch upstream
git pull upstream

# If needing to re-issue a tag:
# git tag -d v${NEW_VERSION}
# git push upstream :refs/tags/v${NEW_VERSION}

# New tag
git tag -a v${NEW_VERSION} -m "Version ${NEW_VERSION}"
git checkout v${NEW_VERSION} # checkout tag you just created

# Test that version output
# matches expected version
python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -e . # Install from local repo

# Verify version number output
TEST_OUTPUT_VERSION=$(create-salt-extension --version | cut -d' ' -f3)
if [[ "${NEW_VERSION}" == "${TEST_OUTPUT_VERSION}" ]]; then
  echo "Version matches! Continuing..."
  deactivate
  rm -rf .venv
  git reset --hard HEAD
  git clean -dfx
  git push upstream v${NEW_VERSION}
  echo "Freshly tagged: v${NEW_VERSION}"
  echo "https://github.com/saltstack/salt-extension/tree/v${NEW_VERSION}"
else
  echo "WARNING: Version of build does not match!"
  echo "Built version output: ${TEST_OUTPUT_VERSION}"
  echo "Expected output: ${NEW_VERSION}"
  echo "Abandoning push of v${NEW_VERSION} tag"
  deactivate
  rm -rf .venv
fi
```

## Generate tarballs

When preparing to generate the tar files, a few pieces need to be taken care of first:

- `umask 022`

> **WARNING:** The `umask 022` needs to be set _**before**_ cloning the repo down and making changes. If that isn't the case, the repo needs to be re-cloned before moving onto the next steps. This is why the directions below ensure this by re-cloning.

```bash
# New tag/version
NEW_VERSION='0.23.0' # Modify to release

# Re-clone repo in fresh dir
mkdir packaging
cd packaging
umask 022
git clone git@github.com:saltstack/salt-extension.git
cd salt-extension

# Clear out cruft, if any
git checkout v${NEW_VERSION}
git reset --hard HEAD
git clean -dfx

# Build for PyPI
# setup.cfg enforces root:root in tarball output
python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
python3 setup.py sdist
twine check dist/*
```

## Uploading to pypi

```bash
# Publish to pypi
twine upload dist/*
```
