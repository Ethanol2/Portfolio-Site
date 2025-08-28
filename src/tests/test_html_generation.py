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
            "<div><p>This is <strong>bolded</strong> paragraph text in a p tag here</p><p>This is another paragraph with <em>italic</em> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        html = markdown_to_html_and_metadata(md)[0]
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
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
            '<div><ol start="1"><li>Item one</li><li>Item two</li><li>Item three</li></ol></div>',
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
        
    def test_simple_container(self):
        md = """\
    ::: note
    This is a note.
    :::
    """
        html, _ = markdown_to_html_and_metadata(md)
        print(html)
        self.assertIn('<div class="note">', html)
        self.assertIn('This is a note.', html)
        self.assertTrue(html.strip().endswith('</div>'))


    def test_nested_containers(self):
        md = """\
    ::: row
    ::: column
    Content A
    :::
    ::: column
    Content B
    :::
    :::
    """
        html, _ = markdown_to_html_and_metadata(md)
        self.assertIn('<div class="row">', html)
        self.assertEqual(html.count('<div class="column">'), 2)
        self.assertIn('Content A', html)
        self.assertIn('Content B', html)


    def test_container_wraps_csv_table(self):
        md = """\
    ::: special-table
    ::: csv
    a,b,c
    1,2,3
    :::
    :::
    """
        html, _ = markdown_to_html_and_metadata(md)
        self.assertIn('<div class="special-table">', html)
        self.assertIn('<table', html)
        self.assertIn('<tr>', html)
        self.assertIn('<td>1</td>', html)


    # def test_multiple_classes_and_attributes(self):
    #     md = """\
    # ::: row large data-info="foo"
    # Hello
    # :::
    # """
    #     html, _ = markdown_to_html_and_metadata(md)
    #     self.assertIn('<div class="row large"', html)
    #     self.assertIn('data-info="foo"', html)
    #     self.assertIn('Hello', html)


    def test_empty_container(self):
        md = """\
    :::
    :::
    """
        html, _ = markdown_to_html_and_metadata(md)
        self.assertTrue('<div>' in html or '<div ' in html)
        self.assertIn('</div>', html)

    def test_csv_block(self):
        md = """\
    ::: csv
    a,b,c
    1,2,3
    4,5,6
    :::
    """
        html, _ = markdown_to_html_and_metadata(md)
        # Expect a table without a thead
        self.assertIn('<table', html)
        self.assertNotIn('<thead>', html)
        self.assertIn('<tr>', html)
        self.assertIn('<td>a</td>', html)
        self.assertIn('<td>1</td>', html)
        self.assertIn('<td>6</td>', html)


    def test_csv_headers_block(self):
        md = """\
    ::: csv_headers
    a,b,c
    1,2,3
    4,5,6
    :::
    """
        html, _ = markdown_to_html_and_metadata(md)
        # Expect a table with a thead and th cells
        self.assertIn('<table', html)
        self.assertIn('<thead>', html)
        self.assertIn('<th>a</th>', html)
        self.assertIn('<th>b</th>', html)
        self.assertIn('<th>c</th>', html)
        self.assertIn('<td>1</td>', html)
        self.assertIn('<td>6</td>', html)

    def test_ordered_list_start_at_one(self):
        md = """1. First
2. Second
3. Third"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="1">'
            "<li>First</li>"
            "<li>Second</li>"
            "<li>Third</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list_start_at_three(self):
        md = """3. Third
4. Fourth"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="3">'
            "<li>Third</li>"
            "<li>Fourth</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list_start_at_ten(self):
        md = """10. Tenth
11. Eleventh"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="10">'
            "<li>Tenth</li>"
            "<li>Eleventh</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list_single_item_high_start(self):
        md = """42. The Answer"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="42">'
            "<li>The Answer</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list_with_gap(self):
        md = """7. First
9. Skipped one"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="7">'
            "<li>First</li>"
            "</ol>"
            '<ol start="9">'
            "<li>Skipped one</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)
    
    def test_simple_nested_ordered_list(self):
        md = """1. First
    1. Sub-first
    2. Sub-second
2. Second"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="1">'
            "<li>First"
            '<ol start="1">'
            "<li>Sub-first</li>"
            "<li>Sub-second</li>"
            "</ol>"
            "</li>"
            "<li>Second</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_mixed_unordered_in_ordered(self):
        md = """1. First
    - Bullet A
    - Bullet B
2. Second"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="1">'
            "<li>First"
            "<ul>"
            "<li>Bullet A</li>"
            "<li>Bullet B</li>"
            "</ul>"
            "</li>"
            "<li>Second</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_nested_multiple_levels(self):
        md = """1. One
    1. One-One
        - Bullet under One-One
    2. One-Two
2. Two"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            '<ol start="1">'
            "<li>One"
            '<ol start="1">'
            "<li>One-One"
            "<ul>"
            "<li>Bullet under One-One</li>"
            "</ul>"
            "</li>"
            "<li>One-Two</li>"
            "</ol>"
            "</li>"
            "<li>Two</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_nested_unordered_list_first(self):
        md = """- A
    1. A-One
    2. A-Two
- B"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<ul>"
            "<li>A"
            '<ol start="1">'
            "<li>A-One</li>"
            "<li>A-Two</li>"
            "</ol>"
            "</li>"
            "<li>B</li>"
            "</ul>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_basic_table(self):
        md = """| Col1 | Col2 |
| ---- | ---- |
| A    | B    |
| C    | D    |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Col1</th><th>Col2</th></tr></thead>"
            "<tbody>"
            "<tr><td align=\"left\">A</td><td align=\"left\">B</td></tr>"
            "<tr><td align=\"left\">C</td><td align=\"left\">D</td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_alignment_table(self):
        md = """| Left | Center | Right |
| :--- | :----: | ----: |
| l1   | c1     | r1    |
| l2   | c2     | r2    |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Left</th><th>Center</th><th>Right</th></tr></thead>"
            "<tbody>"
            "<tr>"
            "<td align=\"left\">l1</td>"
            "<td align=\"center\">c1</td>"
            "<td align=\"right\">r1</td>"
            "</tr>"
            "<tr>"
            "<td align=\"left\">l2</td>"
            "<td align=\"center\">c2</td>"
            "<td align=\"right\">r2</td>"
            "</tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_table_with_extra_spaces(self):
        md = """|  Name   | Value   |
|   ---   |   ---   |
|   Foo   |   Bar   |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Name</th><th>Value</th></tr></thead>"
            "<tbody>"
            "<tr><td align=\"left\">Foo</td><td align=\"left\">Bar</td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_table_with_missing_cells(self):
        md = """| Col1 | Col2 | Col3 |
| ---- | ---- | ---- |
| a    | b    |      |
| c    |      | e    |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Col1</th><th>Col2</th><th>Col3</th></tr></thead>"
            "<tbody>"
            "<tr><td align=\"left\">a</td><td align=\"left\">b</td><td align=\"left\"></td></tr>"
            "<tr><td align=\"left\">c</td><td align=\"left\"></td><td align=\"left\">e</td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_table_with_bold_and_italic(self):
        md = """| Col1 | Col2 |
| ---- | ---- |
| **bold** | _italic_ |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Col1</th><th>Col2</th></tr></thead>"
            "<tbody>"
            "<tr><td align=\"left\"><strong>bold</strong></td><td align=\"left\"><em>italic</em></td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_table_with_inline_code(self):
        md = """| Code |
| ---- |
| `print(1)` |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Code</th></tr></thead>"
            "<tbody>"
            "<tr><td align=\"left\"><code>print(1)</code></td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_table_with_link_and_image(self):
        md = """| Link | Image |
| ---- | ----- |
| [OpenAI](https://openai.com) | ![alt](img.png) |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Link</th><th>Image</th></tr></thead>"
            "<tbody>"
            "<tr>"
            "<td align=\"left\"><a href=\"https://openai.com\">OpenAI</a></td>"
            "<td align=\"left\"><img src=\"img.png\" alt=\"alt\"/></td>"
            "</tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_table_with_nested_formatting(self):
        md = """| Mixed |
| ----- |
| **bold and _italic_ with `code`** |"""
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<table>"
            "<thead><tr><th>Mixed</th></tr></thead>"
            "<tbody>"
            "<tr><td align=\"left\"><strong>bold and <em>italic</em> with <code>code</code></strong></td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        self.assertEqual(html, expected)
    def test_nested_bold_inside_italic(self):
        md = "_This is **bold inside italic** text_"
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            '<div>'
            '<p><em>This is <strong>bold inside italic</strong> text</em></p>'
            '</div>'
        )
        self.assertEqual(html, expected)

    def test_nested_italic_inside_bold(self):
        md = "**This is _italic inside bold_ text**"
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            '<div>'
            '<p><strong>This is <em>italic inside bold</em> text</strong></p>'
            '</div>'
        )
        self.assertEqual(html, expected)

    def test_nested_code_inside_bold(self):
        md = "**Here is `inline code` in bold**"
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            '<div>'
            '<p><strong>Here is <code>inline code</code> in bold</strong></p>'
            '</div>'
        )
        self.assertEqual(html, expected)

    def test_multiple_nested_levels(self):
        md = "_Italic with **bold and `code` inside** text_"
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            '<div>'
            '<p><em>Italic with <strong>bold and <code>code</code> inside</strong> text</em></p>'
            '</div>'
        )
        self.assertEqual(html, expected)

    def test_invalid_overlap_not_nested(self):
        md = "**bold _invalid overlap** still bold_"
        html, _ = markdown_to_html_and_metadata(md)
        expected = (
            "<div>"
            "<p><strong>bold _invalid overlap</strong> still bold_</p>"
            "</div>"
        )
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
