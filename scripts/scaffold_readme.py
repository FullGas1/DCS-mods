"""
scaffold_readme.py — Generate a default README.md for a mod folder.

Reads metadata from the mod ZIP, checks for screenshots in media/,
and writes a README.md if one does not already exist.

Usage:
    python scaffold_readme.py <mod_folder_path>

Exit codes:
    0 — README created
    1 — README already exists (no-op)
    2 — Error (missing ZIP, parse failure, etc.)
"""

import sys
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).parent))
from parse_mod import parse_mod_zip

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def find_first_image(media_dir: Path) -> str | None:
    """Return the relative path to the first image in media/, or None."""
    if not media_dir.is_dir():
        return None
    for f in sorted(media_dir.iterdir()):
        if f.suffix.lower() in IMAGE_EXTENSIONS:
            return f"media/{f.name}"
    return None


def render_readme(metadata: dict, first_image: str | None) -> str:
    """Render the default README template from mod metadata."""
    name = metadata["name"]
    description = metadata["description"] or "<!-- To be completed -->"
    mod_folder = name

    lines = [f"# {name}", ""]

    if first_image:
        lines += [f"![{name} screenshot]({first_image})", ""]

    lines += [
        "## Description",
        "",
        description,
        "",
        "## Installation",
        "",
        "Extract the ZIP and copy the folder to:",
        "",
        f"`..\\Saved Games\\DCS.openbeta\\Mods\\tech\\{mod_folder}`",
        "",
        "## Usage",
        "",
        "<!-- To be completed -->",
        "",
        "## Screenshots / Videos",
        "",
        "<!-- Add links or images from media/ -->",
        "",
    ]

    return "\n".join(lines)


def scaffold(mod_folder: Path) -> bool:
    """
    Generate README.md for a mod folder if it does not already exist.

    Returns True if a README was created, False if it already existed.
    Raises on error.
    """
    readme_path = mod_folder / "README.md"
    if readme_path.exists():
        return False

    zip_path = mod_folder / f"{mod_folder.name}.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"No ZIP found at {zip_path}")

    metadata = parse_mod_zip(str(zip_path))
    first_image = find_first_image(mod_folder / "media")
    content = render_readme(metadata, first_image)
    readme_path.write_text(content, encoding="utf-8")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scaffold_readme.py <mod_folder_path>", file=sys.stderr)
        sys.exit(2)

    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"Error: {folder} is not a directory", file=sys.stderr)
        sys.exit(2)

    try:
        created = scaffold(folder)
        if created:
            print(f"README created: {folder / 'README.md'}")
            sys.exit(0)
        else:
            print(f"README already exists, skipping: {folder / 'README.md'}")
            sys.exit(1)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
