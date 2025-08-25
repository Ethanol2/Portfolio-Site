import unittest
from markdownblock import markdown_to_block_and_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):

    def test_paragraph_single_line(self):
        lines = ["This is a simple paragraph.", "", "Next paragraph here."]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(block, "This is a simple paragraph.")
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        self.assertEqual(remaining, ["", "Next paragraph here."])

    def test_paragraph_multiple_lines(self):
        lines = [
            "This is a paragraph that spans",
            "multiple lines until a blank line is found.",
            "",
            "Second paragraph starts here.",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            "This is a paragraph that spans\nmultiple lines until a blank line is found.",
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        self.assertEqual(remaining, ["", "Second paragraph starts here."])

    def test_heading(self):
        lines = ["## Heading Level 2", "Next line here"]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(block, "## Heading Level 2")
        self.assertEqual(block_type, BlockType.HEADING2)
        self.assertEqual(remaining, ["Next line here"])

    def test_code_block(self):
        lines = [
            "```",
            "def hello():",
            "    return 'world'",
            "```",
            "after code",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            "def hello():\n    return 'world'"
        )
        self.assertEqual(block_type, BlockType.CODE)
        self.assertEqual(remaining, ["after code"])

    def test_quote_block(self):
        lines = [
            "> quote line 1",
            "> quote line 2",
            "not quote",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            "> quote line 1\n> quote line 2",
        )
        self.assertEqual(block_type, BlockType.QUOTE)
        self.assertEqual(remaining, ["not quote"])

    def test_unordered_list(self):
        lines = [
            "- item 1",
            "- item 2",
            "paragraph next",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            ["item 1", "item 2"]
        )
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        self.assertEqual(remaining, ["paragraph next"])

    def test_ordered_list(self):
        lines = [
            "1. first",
            "2. second",
            "another block",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            [1, "first", "second"]
        )
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(remaining, ["another block"])
    
    def test_ordered_list_0_start(self):
        lines = [
            "0. first",
            "1. second",
            "another block",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            [0, "first", "second"]
        )
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(remaining, ["another block"])

    def test_ordered_list_14_start(self):
        lines = [
            "14. first",
            "15. second",
            "another block",
        ]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(
            block,
            [14, "first", "second"]
        )
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(remaining, ["another block"])
    
    def test_paragraph_with_leading_num(self):
        lines = [
            "14 is the number I like most.",
            "1 is the first number, and therefore cool",
            "4 is a nice round even number."
        ]
        block, type, remaining = markdown_to_block_and_type(lines)
        self.assertEqual(block, "14 is the number I like most.\n1 is the first number, and therefore cool\n4 is a nice round even number.")
        self.assertEqual(type, BlockType.PARAGRAPH)
        self.assertEqual(remaining, [])

    def test_empty_lines(self):
        lines = ["", "", "Content after blanks"]
        block, block_type, remaining = markdown_to_block_and_type(lines)
        # blanks should be skipped, so we pick up the paragraph
        self.assertEqual(block, "")
        self.assertEqual(block_type, BlockType.NONE)
        self.assertEqual(remaining, ["", "Content after blanks"])