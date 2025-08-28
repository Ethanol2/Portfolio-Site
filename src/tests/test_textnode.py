import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    
    # Test TextNode Class ==================================================================
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_neq(self):
        node = TextNode("This is one sentence", TextType.ITALIC)
        node2 = TextNode("This is another sentence", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url(self):
        node = TextNode("This node has a URL", TextType.URL, "https://google.ca")
        node2 = TextNode("This node doesn't have a URL", TextType.PLAIN)
        self.assertIsNotNone(node.url)
        self.assertEqual('',node2.url)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, '')
        self.assertEqual(html_node.value, "This is a text node")
    
    # Test Helper Functions ==================================================================
    def test_code_delimiter_split(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        correct_result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertEqual(correct_result, new_nodes)
        
    def test_bold_delimiter_split(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        
        correct_result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertEqual(correct_result, new_nodes)
        
    def test_multiple_delimiters(self):
        test_text = [
            "I'm learning about **backend development** through the website _boot.dev_.",
            " I'm **really** enjoying the courses in their curriculum. The main programming language is `python`.",
            " It's an easy language to learn the _syntax_ of, but because I'm originally a `C++` and `C#` programmer, it took some time to get used to.",
            " One thing that I found **really** annoying was the lack of typing, and the way OOP is done."
        ]
        
        correct_nodes = [
            TextNode("I'm learning about ", TextType.PLAIN),
            TextNode("backend development", TextType.BOLD),
            TextNode(" through the website ", TextType.PLAIN),
            TextNode("boot.dev", TextType.ITALIC),
            TextNode(".", TextType.PLAIN),
            TextNode(" I'm ", TextType.PLAIN),
            TextNode("really", TextType.BOLD),
            TextNode(" enjoying the courses in their curriculum. The main programming language is ", TextType.PLAIN),
            TextNode("python", TextType.CODE),
            TextNode(".", TextType.PLAIN),
            TextNode(" It's an easy language to learn the ", TextType.PLAIN),
            TextNode("syntax", TextType.ITALIC),
            TextNode(" of, but because I'm originally a ", TextType.PLAIN),
            TextNode("C++", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("C#", TextType.CODE),
            TextNode(" programmer, it took some time to get used to.", TextType.PLAIN),
            TextNode(" One thing that I found ", TextType.PLAIN),
            TextNode("really", TextType.BOLD),
            TextNode(" annoying was the lack of typing, and the way OOP is done.", TextType.PLAIN),            
        ]
        
        start_nodes = [TextNode(str(test_text[i]), TextType.PLAIN) for i in range(0, len(test_text))]
        
        # for node in start_nodes:
        #     print("\n")
        #     print(node)
        
        new_nodes = split_nodes_delimiter(start_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
            
        self.assertListEqual(correct_nodes, new_nodes)
    
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png", '')], matches)
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text some images; ![image1](https://i.imgur.com/zjjcJKZ.png), ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image1", "https://i.imgur.com/zjjcJKZ.png", ''),
            ("image2", "https://i.imgur.com/zjjcJKZ.png", '')
            ], matches)
    
    def test_extract_markdown_images_with_tags(self):
        matches = extract_markdown_images(
            "This is text some images; ![image1](https://i.imgur.com/zjjcJKZ.png){class=special-img}, ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image1", "https://i.imgur.com/zjjcJKZ.png", 'class=special-img'),
            ("image2", "https://i.imgur.com/zjjcJKZ.png", '')
            ], matches)
        
    def test_extract_markdown_url(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png", "")], matches)
        
    def test_extract_markdown_urls(self):
        
        matches = extract_markdown_links(
            "This is text some links; [link1](https://i.imgur.com/zjjcJKZ.png), [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("link1", "https://i.imgur.com/zjjcJKZ.png", ""),
            ("link2", "https://i.imgur.com/zjjcJKZ.png", "")
            ], matches)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links_and_images([node])        
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.URL, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.URL, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Test Main Split Function ==================================================================
    def test_basic_formatting(self):
        text = "This is **bold** and _italic_ and a [link](https://site.com)."
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.URL, "https://site.com"),
            TextNode(".", TextType.PLAIN)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_malformed_link_syntax_fallback_to_plain(self):
        text = "Click [here](not-a-url and keep reading."
        expected = [
            TextNode("Click [here](not-a-url and keep reading.", TextType.PLAIN)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_no_formatting_plain_text(self):
        text = "Just a boring plain sentence."
        expected = [
            TextNode("Just a boring plain sentence.", TextType.PLAIN)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)
    
    def test_repeated_identical_links(self):
        text = "Check [here](https://example.com) and again [here](https://example.com)"
        expected = [
            TextNode("Check ", TextType.PLAIN),
            TextNode("here", TextType.URL, "https://example.com"),
            TextNode(" and again ", TextType.PLAIN),
            TextNode("here", TextType.URL, "https://example.com")
        ]
        
        new_nodes = text_to_textnodes(text)
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertListEqual(new_nodes, expected)

    def test_plain_image(self):
        text = "Here is an ![alt text](https://example.com/img.png)"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            'Here is an <img src="https://example.com/img.png" alt="alt text"/>'
        )

    def test_plain_link(self):
        text = "Here is a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            'Here is a <a href="https://example.com">link</a>'
        )

    def test_image_inside_link(self):
        text = "Click this [![alt](https://example.com/img.png)](https://example.com)"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            'Click this <a href="https://example.com"><img src="https://example.com/img.png" alt="alt"/></a>'
        )

    def test_link_with_text_and_image(self):
        text = "[Check this ![alt](https://example.com/img.png)](https://example.com)"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            '<a href="https://example.com">Check this <img src="https://example.com/img.png" alt="alt"/></a>'
        )

    def test_malformed_image(self):
        # Missing closing parenthesis, should fall back to plain text
        text = "Broken ![alt](https://example.com/img.png"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            "Broken ![alt](https://example.com/img.png"
        )

    def test_malformed_link(self):
        # Missing closing bracket, should fall back to plain text
        text = "Broken [link(https://example.com)"
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            "Broken [link(https://example.com)"
        )
    
    def test_image_with_class(self):
        text = 'Here is an ![Img](img.com/img.png){class="special-img"}'
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            'Here is an <img src="img.com/img.png" alt="Img" class="special-img"/>'
        )

    def test_image_with_multiple_attributes(self):
        text = '![Logo](logo.png){class="logo" id="main-logo"}'
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            '<img src="logo.png" alt="Logo" class="logo" id="main-logo"/>'
        )

    def test_image_with_empty_attributes(self):
        text = '![Alt](pic.png){}'
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        # Empty braces should just be ignored
        self.assertEqual(
            html,
            '<img src="pic.png" alt="Alt"/>'
        )

    def test_image_in_link_with_attribute(self):
        text = '[![Alt](pic.png){class="small"}](https://example.com)'
        nodes = text_to_textnodes(text)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        self.assertEqual(
            html,
            '<a href="https://example.com"><img src="pic.png" alt="Alt" class="small"/></a>'
        )        
    
    def test_link_with_attribute(self):
        md = '[Google](https://google.com){target="_blank"}'
        nodes = text_to_textnodes(md)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        expected = '<a href="https://google.com" target="_blank">Google</a>'
        self.assertEqual(html, expected)

    def test_link_with_multiple_attributes(self):
        md = '[Example](https://example.com){class="link" target="_blank"}'
        nodes = text_to_textnodes(md)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        expected = '<a href="https://example.com" class="link" target="_blank">Example</a>'
        self.assertEqual(html, expected)
    
if __name__ == "__main__":
    unittest.main()