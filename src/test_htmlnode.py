import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("tag", "value", ["test"], {"test":"test"})
        node2 = HTMLNode()
        
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.children)
        self.assertIsNotNone(node.props)
        
        self.assertEqual(node2.tag, "")
        self.assertEqual(node2.value, "")
        self.assertEqual(node2.children, [])
        self.assertEqual(node2.props, {})
    
    def test_props(self):
        
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        
        node = HTMLNode(props=props)
        
        html = node.props_to_html()
        
        print(html)
        
        for key in props.keys():
            self.assertTrue(key in html, "If false, the prop key was not included the html")
            self.assertTrue(props[key] in html, "If false, the prop was not included in the html")
    
    def test_repr(self):
        values = [
            "tag",
            "content",
            ["children"],
            {"prop":"prop"}
        ]
        
        node = HTMLNode(*values)
        repr = str(node)
        print(node)
        
        self.assertEqual(f'HTMLNode({values[0]}, {values[1]}, {values[2]}, {values[3]})', repr)

class TestLeafNode(unittest.TestCase):
    def test_p_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")   
        
    def test_a_leaf_to_html(self):        
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})        
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", node.to_html())
        
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )    
    
        
if __name__ == "__main__":
    unittest.main()