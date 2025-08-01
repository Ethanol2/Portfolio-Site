import unittest
from markdownblock import *


class TestMarkdownBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        # for block in blocks:
        #     print("\n")
        #     print(block)

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
        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_two_blocks(self):
        text = "First paragraph.\n\nSecond paragraph."
        expected = ["First paragraph.", "Second paragraph."]
        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_three_blocks_with_extra_newlines(self):
        text = "Para one.\n\n\n\nPara two.\n\nPara three."
        expected = ["Para one.", "Para two.", "Para three."]
        self.assertListEqual(markdown_to_blocks(text), expected)

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
        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_leading_and_trailing_newlines(self):
        text = "\n\nFirst block.\n\nSecond block.\n\n\n"
        expected = ["First block.", "Second block."]
        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_no_blocks_empty_string(self):
        text = ""
        expected = []
        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_only_whitespace_and_newlines(self):
        text = "   \n \n\n  \n"
        expected = []
        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_heading_level_1(self):
        block = "# Heading level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING1)

    def test_heading_level_2(self):
        block = "## Heading level 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING2)

    def test_heading_level_3(self):
        block = "### Heading level 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING3)

    def test_heading_level_4(self):
        block = "#### Heading level 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING4)

    def test_heading_level_5(self):
        block = "##### Heading level 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING5)

    def test_heading_level_6(self):
        block = "###### Heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING6)

    def test_heading_too_many_hashes_fallback(self):
        block = "####### Not a valid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_no_space_fallback(self):
        block = "###HeadingWithoutSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_only_hashes_fallback(self):
        block = "###"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_invalid_too_many_hashes(self):
        block = "####### Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        block = "This is a normal paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Not currently supporting this markdown format for code blocks
    # def test_code_block_with_indentation(self):
    #     block = "    for i in range(10):\n        print(i)"
    #     self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_backticks(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_with_dash(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_indented(self):
        block = "  - Indented item\n  - Another item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_asterisk_list_fallback_to_paragraph(self):
        block = "* Not recognized as a list\n* Under current rules"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. One\n2. Two\n3. Three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_with_numbers_not_list(self):
        block = "2023 was a good year. 1. Not a list item."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        # print("\n")
        # print(repr(html))

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        # print("\n")
        # print(repr(html))

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_single_paragraph(self):
        markdown = "This is a **bold** word and _italic_ too."
        expected_html = (
            "<div><p>This is a <b>bold</b> word and <i>italic</i> too.</p></div>"
        )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_multiple_paragraphs(self):
        markdown = "First paragraph.\n\nSecond paragraph."
        expected_html = "<div><p>First paragraph.</p><p>Second paragraph.</p></div>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_heading_levels(self):
        markdown = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        expected_html = (
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_ordered_list(self):
        markdown = "1. Item one\n2. Item two\n3. Item three"
        expected_html = (
            "<div><ol><li>Item one</li><li>Item two</li><li>Item three</li></ol></div>"
        )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_unordered_list(self):
        markdown = "- Apple\n- Banana\n- Cherry"
        expected_html = (
            "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>"
        )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_blockquote(self):
        markdown = "> This is a quote.\n> It has two lines."
        expected_html = (
            "<div><blockquote>This is a quote.\nIt has two lines.</blockquote></div>"
        )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_code_block_backticks(self):
        markdown = "```\ndef hello():\n    return 'world'\n```"
        expected_html = (
            "<div><pre><code>def hello():\n    return 'world'\n</code></pre></div>"
        )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

    def test_links_and_images(self):
        markdown = "Here is a [link](https://example.com) and an ![image](https://img.com/img.png)"
        expected_html = '<div><p>Here is a <a href="https://example.com">link</a> and an <img src="https://img.com/img.png" alt="image"/></p></div>'
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected_html)

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

    # Test Youtube Links
    def test_youtube_markdown_embed_watch_link(self):
        markdown = "@[youtube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        node = markdown_to_html_node(markdown)
        expected_html = (
            '<div><p><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" '
            "allowfullscreen></iframe></p></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_youtube_markdown_embed_direct_embed_url(self):
        markdown = "@[youtube](https://www.youtube.com/embed/dQw4w9WgXcQ)"
        node = markdown_to_html_node(markdown)
        expected_html = (
            '<div><p><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" '
            "allowfullscreen></iframe></p></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    # Test CSV
    def test_csv_markdown_table_with_quotes(self):
        markdown = (
            ":::csv\n"
            '"Name","Role"\n'
            '"Alice, A.","Editor"\n'
            '"Bob","Author"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><td>Name</td><td>Role</td></tr>"
            "<tr><td>Alice, A.</td><td>Editor</td></tr>"
            "<tr><td>Bob</td><td>Author</td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_markdown_table_with_headers_and_quotes(self):
        markdown = (
            ":::csv_headers\n"
            '"Name","Role"\n'
            '"Alice, A.","Editor"\n'
            '"Bob","Author"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Name</th><th>Role</th></tr>"
            "<tr><td>Alice, A.</td><td>Editor</td></tr>"
            "<tr><td>Bob</td><td>Author</td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_markdown_table_with_line_breaks_in_cells(self):
        markdown = (
            ":::csv_headers\n"
            '"Name","Bio"\n'
            '"Alice","Editor\nLoves Markdown"\n'
            '"Bob","Author\nWrites daily."\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Name</th><th>Bio</th></tr>"
            "<tr><td>Alice</td><td>Editor<br>Loves Markdown</td></tr>"
            "<tr><td>Bob</td><td>Author<br>Writes daily.</td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
