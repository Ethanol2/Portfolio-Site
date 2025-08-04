import unittest
from markdownblock import markdown_to_html_node


class TestCSVMarkdown(unittest.TestCase):

    def test_csv_markdown_table_with_quotes(self):
        markdown = (
            ":::csv\n"
            '"**Name**","Role"\n'
            '"Alice, A.","_Editor_"\n'
            '"Bob","`Author`"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><td><b>Name</b></td><td>Role</td></tr>"
            "<tr><td>Alice, A.</td><td><i>Editor</i></td></tr>"
            "<tr><td>Bob</td><td><code>Author</code></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_markdown_table_with_headers_and_quotes(self):
        markdown = (
            ":::csv_headers\n"
            '"**Name**","_Role_"\n'
            '"Alice, A.","**Editor**"\n'
            '"Bob","`Author`"\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th><b>Name</b></th><th><i>Role</i></th></tr>"
            "<tr><td>Alice, A.</td><td><b>Editor</b></td></tr>"
            "<tr><td>Bob</td><td><code>Author</code></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_markdown_table_with_line_breaks_in_cells(self):
        markdown = (
            ":::csv_headers\n"
            '"Name","Bio"\n'
            '"Alice","Editor\n**Loves** _Markdown_"\n'
            '"Bob","Author\nWrites `daily`."\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Name</th><th>Bio</th></tr>"
            "<tr><td>Alice</td><td>Editor<br><b>Loves</b> <i>Markdown</i></td></tr>"
            "<tr><td>Bob</td><td>Author<br>Writes <code>daily</code>.</td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_paragraphs(self):
        markdown = (
            ":::csv_headers\n"
            '"Name","Details"\n'
            '"Alice","First line.\n\nSecond paragraph."\n'
            ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Name</th><th>Details</th></tr>"
            "<tr><td>Alice</td><td><p>First line.</p><p>Second paragraph.</p></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_csv_cell_with_list(self):
        markdown = (
            ":::csv_headers\n"
            '"Item","Features"\n'
            '"Widget","- Small\n- Lightweight\n- Durable"\n'
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
            '"Python","```\ndef hello():\n    return True\n```"\n'
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
            ":::csv_headers\n" '"Person","Quote"\n' '"Bob","> Keep it simple."\n' ":::"
        )
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div><table>"
            "<tr><th>Person</th><th>Quote</th></tr>"
            "<tr><td>Bob</td><td><blockquote>Keep it simple.</blockquote></td></tr>"
            "</table></div>"
        )
        self.assertEqual(node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
