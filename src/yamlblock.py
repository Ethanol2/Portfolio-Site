import yaml

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType

def yaml_to_html_node(block: str) -> ParentNode:
    
    parsed = yaml.parse(block, yaml.loader.FullLoader)
    
    return ParentNode("div", [])