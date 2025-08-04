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
        self.assertIsNone(node2.url)
        
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
        
    def test_bad_bold_delimiter_split(self):
        node = TextNode("This is text with a **bold block word", TextType.PLAIN)
        
        with self.assertRaises(Exception): split_nodes_delimiter([node], "**", TextType.CODE)
        
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
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text some images; ![image1](https://i.imgur.com/zjjcJKZ.png), ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image1", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "https://i.imgur.com/zjjcJKZ.png")
            ], matches)
        
    def test_extract_markdown_url(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_urls(self):
        
        matches = extract_markdown_links(
            "This is text some links; [link1](https://i.imgur.com/zjjcJKZ.png), [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("link1", "https://i.imgur.com/zjjcJKZ.png"),
            ("link2", "https://i.imgur.com/zjjcJKZ.png")
            ], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_images([node])        
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])        
        
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
    def test_general_split_one(self):
        
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        correct_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.URL, "https://boot.dev"),
        ]
        
        self.assertListEqual(new_nodes, correct_nodes)
    
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

    def test_image_and_formatting(self):
        text = "![logo](https://img.com/logo.png) Welcome to the **Show**!"
        expected = [
            TextNode("logo", TextType.IMAGE, "https://img.com/logo.png"),
            TextNode(" Welcome to the ", TextType.PLAIN),
            TextNode("Show", TextType.BOLD),
            TextNode("!", TextType.PLAIN)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_link_and_image_mixed(self):
        text = "Visit [GitHub](https://github.com) and see ![icon](https://img.com/icon.png)"
        expected = [
            TextNode("Visit ", TextType.PLAIN),
            TextNode("GitHub", TextType.URL, "https://github.com"),
            TextNode(" and see ", TextType.PLAIN),
            TextNode("icon", TextType.IMAGE, "https://img.com/icon.png")
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_unclosed_bold_raises(self):
        text = "This is **bold text with no end and plain after"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_malformed_image_syntax_fallback_to_plain(self):
        text = "Here’s an image ![alt text(https://bad.com/img.png)"
        expected = [
            TextNode("Here’s an image ![alt text(https://bad.com/img.png)", TextType.PLAIN)
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
    
    def test_repeated_identical_images(self):
        text = "This is the same text once ![image](https://www.img.com/img) and twice ![image](https://www.img.com/img)"
        expected = [
            TextNode("This is the same text once ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://www.img.com/img"),
            TextNode(" and twice ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://www.img.com/img")
        ]
        
        new_nodes = text_to_textnodes(text)
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertListEqual(new_nodes, expected)

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

    
    
if __name__ == "__main__":
    unittest.main()