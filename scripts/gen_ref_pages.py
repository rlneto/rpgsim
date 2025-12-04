"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("core/systems").rglob("facade.py")):
    module_path = path.relative_to(".").with_suffix("")
    system_name = path.parent.name
    doc_path = Path(f"{system_name}.md")
    full_doc_path = Path("reference", doc_path)

    nav_parts = (system_name,)

    nav[nav_parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(module_path.parts)
        print(f"# {system_name.replace('_', ' ').title()}", file=fd)
        print(f"::: {identifier}", file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
