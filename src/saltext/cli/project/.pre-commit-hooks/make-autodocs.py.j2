import sys
from enum import IntEnum
from pathlib import Path


class Result(IntEnum):
    success = 0
    fail = 1


result = Result.fail

all_states = []
all_mods = []
docs_path = Path("docs")
ref_path = docs_path / "ref"
mod_path = ref_path / "modules"
state_path = ref_path / "states"

for path in Path("src").glob("**/*.py"):
    if path.parent.name in ("states", "modules"):
        kind = path.parent.name
        import_path = ".".join(path.with_suffix("").parts[1:])
        if kind == "states":
            all_states.append(import_path)
            rst_path = state_path / (import_path + ".rst")
        elif kind == "modules":
            all_mods.append(import_path)
            rst_path = mod_path / (import_path + ".rst")

        rst_path.parent.mkdir(parents=True, exist_ok=True)
        rst_path.write_text(
            f"""
{import_path}
{'='*len(import_path)}

.. automodule:: {import_path}
    :members:
"""
        )

        # print(import_path)
        # print(kind, path)

states_rst = state_path / "all.rst"
states_rst.parent.mkdir(parents=True, exist_ok=True)
mods_rst = mod_path / "all.rst"
mods_rst.parent.mkdir(parents=True, exist_ok=True)


mods_rst.write_text(
    f"""
.. all-saltext.vmware.modules:

-----------------
Execution Modules
-----------------

.. autosummary::
    :toctree:

{chr(10).join(sorted('    '+mod for mod in all_mods))}
"""
)
states_rst.write_text(
    f"""
.. all-saltext.vmware.states:

-------------
State Modules
-------------

.. autosummary::
    :toctree:

{chr(10).join(sorted('    '+state for state in all_states))}
"""
)
# exit(result)
