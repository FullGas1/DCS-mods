"""Unit tests for parse_mod.py"""

import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from parse_mod import parse_entry_lua, parse_mod_zip

FIXTURES = Path(__file__).parent / "fixtures"


def _make_zip(lua_content: str) -> str:
    """Create an in-memory ZIP containing entry.lua and return its path via a temp file."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("FG_test_mod/entry.lua", lua_content)
    buf.seek(0)
    return buf


class TestParseEntryLua(unittest.TestCase):

    def test_dcs_version_constant_returns_dcs_compatible(self):
        lua = (FIXTURES / "single_plugin_dcs_version.lua").read_text(encoding="utf-8")
        result = parse_entry_lua(lua)
        self.assertEqual(result["version"], "DCS compatible")

    def test_literal_version_returned_as_is(self):
        lua = (FIXTURES / "single_plugin_literal_version.lua").read_text(encoding="utf-8")
        result = parse_entry_lua(lua)
        self.assertEqual(result["version"], "2.7")

    def test_multi_plugin_uses_first_declare_plugin_only(self):
        lua = (FIXTURES / "multi_plugin.lua").read_text(encoding="utf-8")
        result = parse_entry_lua(lua)
        self.assertEqual(result["name"], "FG_small_Helipad")
        self.assertEqual(result["version"], "DCS compatible")

    def test_all_fields_extracted(self):
        lua = (FIXTURES / "single_plugin_literal_version.lua").read_text(encoding="utf-8")
        result = parse_entry_lua(lua)
        self.assertEqual(result["name"], "FG_sample_Cargo")
        self.assertEqual(result["developerName"], "FullGas")
        self.assertEqual(result["description"], "Sample cargo crate.")
        self.assertEqual(result["category"], "Cargo")

    def test_no_declare_plugin_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_entry_lua("-- empty lua file\n")

    def test_missing_category_defaults_to_misc(self):
        lua = 'declare_plugin("X", { installed = true, developerName = "A", version = "1.0", description = "test", })'
        result = parse_entry_lua(lua)
        self.assertEqual(result["category"], "Misc")


class TestParseModZip(unittest.TestCase):

    def _make_zip_file(self, lua_content: str, tmp_path: Path) -> str:
        zip_path = tmp_path / "test_mod.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("test_mod/entry.lua", lua_content)
        return str(zip_path)

    def test_parses_zip_correctly(self):
        import tempfile, os
        lua = (FIXTURES / "single_plugin_dcs_version.lua").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "FG_small_Helipad.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("FG_small_Helipad/entry.lua", lua)
            result = parse_mod_zip(zip_path)
        self.assertEqual(result["name"], "FG_small_Helipad")
        self.assertEqual(result["version"], "DCS compatible")

    def test_zip_without_entry_lua_raises_file_not_found(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "empty_mod.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("readme.txt", "no lua here")
            with self.assertRaises(FileNotFoundError):
                parse_mod_zip(zip_path)


if __name__ == "__main__":
    unittest.main()
