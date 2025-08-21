import unittest
from markdownblock import markdown_to_html_and_metadata


class TestHtmlGeneration(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        html = markdown_to_html_and_metadata(md)[0]
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        html = markdown_to_html_and_metadata(md)[0]
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists_headings_quotes(self):
        self.assertEqual(
            markdown_to_html_and_metadata(
                "# Heading 1\n\n## Heading 2\n\n### Heading 3"
            )[0],
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )
        self.assertEqual(
            markdown_to_html_and_metadata("- Apple\n- Banana\n- Cherry")[0],
            "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>",
        )
        self.assertEqual(
            markdown_to_html_and_metadata("1. Item one\n2. Item two\n3. Item three")[0],
            "<div><ol><li>Item one</li><li>Item two</li><li>Item three</li></ol></div>",
        )
        self.assertEqual(
            markdown_to_html_and_metadata("> This is a quote.\n> It has two lines.")[0],
            "<div><blockquote>This is a quote.\nIt has two lines.</blockquote></div>",
        )

    def test_links_and_images(self):
        md = "Here is a [link](https://example.com) and an ![image](https://img.com/img.png)"
        html = markdown_to_html_and_metadata(md)[0]
        expected = '<div><p>Here is a <a href="https://example.com">link</a> and an <img src="https://img.com/img.png" alt="image"/></p></div>'
        self.assertEqual(html, expected)

    def test_horizontal_rules(self):
        self.assertEqual(markdown_to_html_and_metadata("---")[0], "<div><hr></div>")
        self.assertEqual(
            markdown_to_html_and_metadata("   ---   ")[0], "<div><hr></div>"
        )
        self.assertEqual(
            markdown_to_html_and_metadata("Above\n\n---\n\nBelow")[0],
            "<div><p>Above</p><hr><p>Below</p></div>",
        )
    def test_image_link(self):
        md = '[![alt text](https://example.com/image.png)](https://example.com)'
        html = markdown_to_html_and_metadata(md)[0]
        expected = (
            '<div>'
            '<p>'
            '<a href="https://example.com">'
            '<img src="https://example.com/image.png" alt="alt text"/>'
            '</a>'
            '</p>'
            '</div>'
        )
        self.assertEqual(html, expected)

    def test_multiple_image_links(self):
        md = (
            '[![img1](https://example.com/1.png)](https://example.com/one) '
            'and '
            '[![img2](https://example.com/2.png)](https://example.com/two)'
        )
        html = markdown_to_html_and_metadata(md)[0]
        expected = (
            '<div>'
            '<p>'
            '<a href="https://example.com/one">'
            '<img src="https://example.com/1.png" alt="img1"/>'
            '</a> and '
            '<a href="https://example.com/two">'
            '<img src="https://example.com/2.png" alt="img2"/>'
            '</a>'
            '</p>'
            '</div>'
        )
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
