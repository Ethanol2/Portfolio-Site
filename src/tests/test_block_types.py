import unittest
from markdownblock import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_levels(self):
        for level in range(1, 7):
            hashes = "#" * level
            block = f"{hashes} Heading level {level}"
            expected = getattr(BlockType, f"HEADING{level}")
            self.assertEqual(block_to_block_type(block), expected)

    def test_heading_fallbacks(self):
        self.assertEqual(
            block_to_block_type("####### Not a valid heading"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("###HeadingWithoutSpace"), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type("###"), BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        block = "This is a normal paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_with_backticks(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- First item\n- Second item\n- Third item"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("  - Indented item\n  - Another item"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("* Not recognized as a list\n* Under current rules"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. One\n2. Two\n3. Three"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("2023 was a good year. 1. Not a list item."),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
