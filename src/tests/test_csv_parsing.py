import unittest
from markdownblock import markdown_to_html_node


class TestCSVMarkdownParsing(unittest.TestCase):

    def test_csv_plain_text(self):
        markdown = (
            ":::csv\n" '"Name","Role"\n' '"Alice","Editor"\n' '"Bob","Author"\n' ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><td>Name</td><td>Role</td></tr>"
            "<tr><td>Alice</td><td>Editor</td></tr>"
            "<tr><td>Bob</td><td>Author</td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_headers_plain_text(self):
        markdown = (
            ":::csv_headers\n"
            '"Name","Role"\n'
            '"Alice","Editor"\n'
            '"Bob","Author"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Name</th><th>Role</th></tr>"
            "<tr><td>Alice</td><td>Editor</td></tr>"
            "<tr><td>Bob</td><td>Author</td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_paragraphs(self):
        markdown = (
            ":::csv\n"
            '"Name","Details"\n'
            '"Alice",md"First line.\n\nSecond paragraph."\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><td>Name</td><td>Details</td></tr>"
            "<tr><td>Alice</td><td><p>First line.</p><p>Second paragraph.</p></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_list(self):
        markdown = (
            ":::csv_headers\n"
            '"Item","Features"\n'
            '"Widget",md"- Small\n- Lightweight\n- Durable"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Item</th><th>Features</th></tr>"
            "<tr><td>Widget</td><td><ul><li>Small</li><li>Lightweight</li><li>Durable</li></ul></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_code_block(self):
        markdown = (
            ":::csv_headers\n"
            '"Language","Example"\n'
            '"Python",md"```\ndef hello():\n    return True\n```"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Language</th><th>Example</th></tr>"
            "<tr><td>Python</td><td><pre><code>def hello():\n    return True\n</code></pre></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_blockquote(self):
        markdown = (
            ":::csv_headers\n" '"Person","Quote"\n' '"Bob",md"> Stay focused."\n' ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Person</th><th>Quote</th></tr>"
            "<tr><td>Bob</td><td><blockquote>Stay focused.</blockquote></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_header_and_list(self):
        markdown = (
            ":::csv_headers\n"
            '"Name","Details"\n'
            'md"# Alice", md"- Editor\n- Loves Markdown"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Name</th><th>Details</th></tr>"
            "<tr><td><h1>Alice</h1></td><td><ul><li>Editor</li><li>Loves Markdown</li></ul></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_heading_and_list_in_same_cell(self):
        markdown = (
            ":::csv_headers\n"
            '"Profile"\n'
            'md"## Alice\n- Editor\n- Markdown Enthusiast"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Profile</th></tr>"
            "<tr><td><h2>Alice</h2><ul><li>Editor</li><li>Markdown Enthusiast</li></ul></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
