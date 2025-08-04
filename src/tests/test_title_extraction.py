import unittest
from markdownblock import markdown_to_html_node, extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extracts_title_from_h1(self):
        markdown = "# This is the Title\n\nSome paragraph text."
        parent_node = markdown_to_html_node(markdown)
        self.assertEqual(extract_title(parent_node), "This is the Title")

    def test_ignores_lower_heading_levels(self):
        markdown = "## Not the Title\n\n### Also not the Title\n\nRegular text."
        parent_node = markdown_to_html_node(markdown)
        with self.assertRaises(Exception):
            extract_title(parent_node)

    def test_throws_exception_if_no_headings(self):
        markdown = "Just a regular paragraph.\n\nAnother paragraph."
        parent_node = markdown_to_html_node(markdown)
        with self.assertRaises(Exception):
            extract_title(parent_node)

    def test_uses_first_h1_only(self):
        markdown = "# First Title\n\n# Second Title\n\nParagraph."
        parent_node = markdown_to_html_node(markdown)
        self.assertEqual(extract_title(parent_node), "First Title")

    def test_ignores_inline_formatting_in_h1(self):
        markdown = "# This is **bold** and _italic_ in a title"
        parent_node = markdown_to_html_node(markdown)
        self.assertEqual(
            extract_title(parent_node), "This is bold and italic in a title"
        )


if __name__ == "__main__":
    unittest.main()
