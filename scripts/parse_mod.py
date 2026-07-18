"""
parse_mod.py — Extract metadata from a DCS mod ZIP file.

Reads entry.lua from the ZIP, parses the first declare_plugin() call,
and outputs structured metadata as JSON.

Usage:
    python parse_mod.py <path/to/mod.zip>

Output (stdout):
    {
        "name": "FG_small_Helipad",
        "developerName": "FullGas",
        "version": "DCS compatible",
        "description": "Small metal helipad for ground placement.",
        "category": "Helipad"
    }
"""

import json
import re
import sys
import zipfile
from pathlib import Path


# Lua identifiers (not string literals) that mean "no fixed version"
_LUA_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# Matches the first declare_plugin("name", { ... }) block
_DECLARE_PLUGIN_RE = re.compile(
    r'declare_plugin\s*\(\s*"([^"]+)"\s*,\s*\{([^}]*)\}',
    re.DOTALL,
)

# Matches key = "string value" or key = identifier
_FIELD_RE = re.compile(
    r"""(\w+)\s*=\s*(?:"([^"]*)"|([\w.]+))""",
    re.DOTALL,
)


def _parse_fields(block: str) -> dict:
    """Return a flat dict of all key=value pairs found in a Lua table block."""
    result = {}
    for match in _FIELD_RE.finditer(block):
        key, str_val, ident_val = match.group(1), match.group(2), match.group(3)
        result[key] = str_val if str_val is not None else ident_val
    return result


def parse_entry_lua(lua_source: str) -> dict:
    """
    Parse the first declare_plugin() call from entry.lua source.

    Returns a dict with keys: name, developerName, version, description, category.
    Raises ValueError if no declare_plugin() block is found.
    """
    match = _DECLARE_PLUGIN_RE.search(lua_source)
    if not match:
        raise ValueError("No declare_plugin() call found in entry.lua")

    plugin_name = match.group(1)
    fields = _parse_fields(match.group(2))

    raw_version = fields.get("version", "")
    version = (
        "DCS compatible"
        if not raw_version or _LUA_IDENTIFIER.match(raw_version)
        else raw_version
    )

    return {
        "name": plugin_name,
        "developerName": fields.get("developerName", ""),
        "version": version,
        "description": fields.get("description", ""),
        "category": fields.get("category", "Misc"),
    }


def parse_mod_zip(zip_path: str) -> dict:
    """
    Open a mod ZIP, find entry.lua, and return parsed metadata.

    Raises FileNotFoundError if the ZIP does not contain entry.lua.
    """
    with zipfile.ZipFile(zip_path, "r") as zf:
        entry_lua_names = [n for n in zf.namelist() if Path(n).name == "entry.lua"]
        if not entry_lua_names:
            raise FileNotFoundError(f"No entry.lua found in {zip_path}")
        lua_source = zf.read(entry_lua_names[0]).decode("utf-8", errors="replace")

    return parse_entry_lua(lua_source)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_mod.py <path/to/mod.zip>", file=sys.stderr)
        sys.exit(1)

    try:
        metadata = parse_mod_zip(sys.argv[1])
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
