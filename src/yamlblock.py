import os
from yaml import safe_load
from urllib.parse import urlparse

from htmlnode import ParentNode, LeafNode, ImageLeafNode, HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node

def yaml_to_html_node(block: str) -> HTMLNode:
    
    parsed = safe_load(block)
    
    return create_html_recursive(parsed)

def create_html_recursive(data, key: str = '') -> HTMLNode:
    
    children = []
    
    if isinstance(key, (dict, list)):
        return create_html_recursive(key)
    
    if isinstance(data, dict):
        
        if key == '':
            key = next(iter(data))
            
        if ('.html' in key) or ('./' in key) or ('mailto:' in key) or ('tel:' in key) or (uri_validator(key)):
            return parse_link(data[key], key)
        
        if ('img' in key):
            parent_node = create_parent_node(key)
            parent_node.props |= data[key]
            return parent_node        
            
        parent_node = create_parent_node(key)
        
        if isinstance(data[key], dict):       
            for item in data[key]:
                children.append(create_html_recursive(data[key], item))
        else:
            for item in data[key]:
                children.append(create_html_recursive(item))
                
        parent_node.children = children
        return parent_node
    
    elif isinstance(data, list):
        parent_node = create_parent_node(key)
        
        for item in data:
            children.append(create_html_recursive(item))
        parent_node.children = children
        return parent_node
    
    elif isinstance(data, str):
        if is_html_tag(data):
            return LeafNode(data, '')
        return LeafNode('', data)
    
    raise NotImplementedError(data)
    
        
def create_parent_node(tag_class: str) -> ParentNode:
    item_split = tag_class.split('.', 1)
                
    props = {}
    if len(item_split) > 1:
        props = {"class":item_split[1]}
    
    return ParentNode(
        tag = item_split[0],
        childen = [],
        props = props
    )
    
def parse_link(data, uri: str) -> HTMLNode:
    
    text_node = TextNode('', TextType.URL, uri)
    
    if isinstance(data, str):
        text_node.text = data
        
    elif isinstance(data, dict):
        
        if data.get('img') != None:
            text_node.text += ImageLeafNode(data['img']).to_html()
            
        if data.get('label') != None:
            text_node.text += create_html_recursive(data['label']).to_html()
            
    return text_node_to_html_node(text_node)

# Source: https://stackoverflow.com/a/38020041
def uri_validator(x) -> bool:
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
    
# Return True if the string looks like a valid HTML tag name.
# ChatGPT function
def is_html_tag(s: str) -> bool:
    html_tags = {
        "a", "abbr", "address", "area", "article", "aside", "audio",
        "b", "base", "bdi", "bdo", "blockquote", "body", "br", "button",
        "canvas", "caption", "cite", "code", "col", "colgroup",
        "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt",
        "em", "embed",
        "fieldset", "figcaption", "figure", "footer", "form",
        "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html",
        "i", "iframe", "img", "input", "ins",
        "kbd", "label", "legend", "li", "link",
        "main", "map", "mark", "meta", "meter",
        "nav", "noscript",
        "object", "ol", "optgroup", "option", "output",
        "p", "param", "picture", "pre", "progress",
        "q",
        "rp", "rt", "ruby",
        "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup",
        "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track",
        "u", "ul",
        "var", "video",
        "wbr"
    }
    return s in html_tags
