import unittest
from markdownblock import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import PassthroughLeafNode  # adjust import if needed

class TestPassthroughInline(unittest.TestCase):
    def test_single_passthrough_node(self):
        text = "This is {<b>}bold{</b>} text"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        self.assertEqual(
            [n.to_html() for n in nodes],
            ["This is ", "<b>", "bold", "</b>", " text"]
        )
        self.assertIsInstance(nodes[1], PassthroughLeafNode)
        self.assertIsInstance(nodes[3], PassthroughLeafNode)

    def test_passthrough_at_start_and_end(self):
        text = "{<i>}Italicized{</i>}"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(html, "<i>Italicized</i>")

    def test_multiple_passthroughs(self):
        text = "Hello {<span>}world{</span>} and {<div>}block{</div>}"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(html, "Hello <span>world</span> and <div>block</div>")

    def test_nested_braces_not_supported(self):
        text = "Outer {<b>{inner}</b>} test"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        # parser should treat the inner `{inner}` literally, not as passthrough
        self.assertEqual(html, "Outer <b>{inner}</b> test")

    def test_empty_passthrough(self):
        text = "Test {} passthrough"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(html, "Test  passthrough")
