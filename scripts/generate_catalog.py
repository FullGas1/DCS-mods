"""
generate_catalog.py — Rebuild the root README.md catalog from all mod folders.

Scans top-level directories for [folder_name].zip, parses each mod's entry.lua,
and produces a README.md grouped by category (alphabetical).

Usage:
    python scripts/generate_catalog.py [repo_root]

    repo_root defaults to the parent of the scripts/ directory.

Exit codes:
    0 — catalog written (content changed)
    1 — catalog unchanged (no write needed)
    2 — error
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_mod import parse_mod_zip

AUTHOR = "FullGas"

HEADER = f"""\
# DCS Mods — {AUTHOR}

> Mods for DCS World. To install a mod, extract the ZIP and copy the folder to:
>
> `..\\Saved Games\\DCS.openbeta\\Mods\\tech\\[mod_name]`

"""

TABLE_HEADER = """\
| Mod | Description | Version |
|-----|-------------|---------|
"""


def collect_mods(repo_root: Path) -> list[dict]:
    """Scan repo root for mod folders and return list of metadata dicts."""
    mods = []
    for folder in sorted(repo_root.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name.startswith(".") or folder.name in ("scripts", ".github"):
            continue
        zip_path = folder / f"{folder.name}.zip"
        if not zip_path.exists():
            continue
        try:
            metadata = parse_mod_zip(str(zip_path))
            metadata["folder"] = folder.name
            mods.append(metadata)
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: skipping {folder.name}: {e}", file=sys.stderr)
    return mods


def build_catalog(mods: list[dict]) -> str:
    """Build the full README.md content from a list of mod metadata dicts."""
    # Group by category
    by_category: dict[str, list[dict]] = {}
    for mod in mods:
        cat = mod.get("category", "Misc")
        by_category.setdefault(cat, []).append(mod)

    lines = [HEADER]

    for category in sorted(by_category.keys()):
        lines.append(f"## {category}\n")
        lines.append(TABLE_HEADER)
        for mod in sorted(by_category[category], key=lambda m: m["name"]):
            name = mod["name"]
            folder = mod["folder"]
            description = mod.get("description", "")
            version = mod.get("version", "—")
            lines.append(f"| [{name}](./{folder}) | {description} | {version} |\n")
        lines.append("\n")

    return "".join(lines)


def main(repo_root: Path) -> int:
    readme_path = repo_root / "README.md"
    mods = collect_mods(repo_root)

    if not mods:
        print("No mods found.", file=sys.stderr)
        return 2

    new_content = build_catalog(mods)

    if readme_path.exists() and readme_path.read_text(encoding="utf-8") == new_content:
        print("Catalog unchanged.")
        return 1

    readme_path.write_text(new_content, encoding="utf-8")
    print(f"Catalog written: {readme_path} ({len(mods)} mod(s))")
    return 0


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    sys.exit(main(root))
