"""Unit tests for scaffold_readme.py — multi-screenshot rendering."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scaffold_readme import find_images, render_readme

METADATA = {
    "name": "FG_test_mod",
    "developerName": "FullGas",
    "version": "DCS compatible",
    "description": "A test mod.",
    "category": "Misc",
}


class TestRenderReadme(unittest.TestCase):

    def test_zero_images(self):
        output = render_readme(METADATA, [])
        self.assertNotIn("![", output.split("## Description")[0])
        self.assertIn("<!-- Add links or images from media/ -->", output)

    def test_one_image_appears_at_top_only(self):
        output = render_readme(METADATA, ["media/shot_01.jpg"])
        top, bottom = output.split("## Description", 1)
        self.assertIn("media/shot_01.jpg", top)
        # Not duplicated in Screenshots section
        screenshots_section = bottom.split("## Screenshots / Videos", 1)[1]
        self.assertNotIn("media/shot_01.jpg", screenshots_section)

    def test_two_images_first_at_top_second_in_section(self):
        output = render_readme(METADATA, ["media/shot_01.jpg", "media/shot_02.jpg"])
        top, bottom = output.split("## Description", 1)
        screenshots_section = bottom.split("## Screenshots / Videos", 1)[1]
        self.assertIn("media/shot_01.jpg", top)
        self.assertNotIn("media/shot_02.jpg", top)
        self.assertIn("media/shot_02.jpg", screenshots_section)

    def test_three_images_first_at_top_rest_in_section(self):
        images = ["media/a.jpg", "media/b.jpg", "media/c.jpg"]
        output = render_readme(METADATA, images)
        top, bottom = output.split("## Description", 1)
        screenshots_section = bottom.split("## Screenshots / Videos", 1)[1]
        self.assertIn("media/a.jpg", top)
        self.assertNotIn("media/b.jpg", top)
        self.assertNotIn("media/c.jpg", top)
        self.assertIn("media/b.jpg", screenshots_section)
        self.assertIn("media/c.jpg", screenshots_section)

    def test_video_placeholder_always_present(self):
        for images in [[], ["media/a.jpg"], ["media/a.jpg", "media/b.jpg"]]:
            output = render_readme(METADATA, images)
            self.assertIn("<!-- Add links or images from media/ -->", output)

    def test_extra_images_in_alphabetical_order(self):
        images = ["media/c.jpg", "media/a.jpg", "media/b.jpg"]
        output = render_readme(METADATA, images)
        screenshots_section = output.split("## Screenshots / Videos", 1)[1]
        pos_a = screenshots_section.find("media/a.jpg")
        pos_b = screenshots_section.find("media/b.jpg")
        self.assertLess(pos_a, pos_b)


class TestFindImages(unittest.TestCase):

    def test_no_media_dir_returns_empty(self):
        result = find_images(Path("/nonexistent/media"))
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
