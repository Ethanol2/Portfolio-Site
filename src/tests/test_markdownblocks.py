import unittest
from markdownblock import markdown_to_blocks_and_metadata


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks_and_metadata(md)[0]
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        text = "This is a single paragraph with **bold** and _italic_."
        expected = ["This is a single paragraph with **bold** and _italic_."]
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)

    def test_two_blocks(self):
        text = "First paragraph.\n\nSecond paragraph."
        expected = ["First paragraph.", "Second paragraph."]
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)

    def test_three_blocks_with_extra_newlines(self):
        text = "Para one.\n\n\n\nPara two.\n\nPara three."
        expected = ["Para one.", "Para two.", "Para three."]
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)

    def test_blocks_with_mixed_content(self):
        text = (
            "# Heading\nSome text here.\n\n"
            "![img](https://img.com)\n\n"
            "Another block with [a link](https://example.com)."
        )
        expected = [
            "# Heading\nSome text here.",
            "![img](https://img.com)",
            "Another block with [a link](https://example.com).",
        ]
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)

    def test_leading_and_trailing_newlines(self):
        text = "\n\nFirst block.\n\nSecond block.\n\n\n"
        expected = ["First block.", "Second block."]
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)

    def test_no_blocks_empty_string(self):
        text = ""
        expected = []
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)

    def test_only_whitespace_and_newlines(self):
        text = "   \n \n\n  \n"
        expected = []
        self.assertListEqual(markdown_to_blocks_and_metadata(text)[0], expected)
