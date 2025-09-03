import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode, ImageLeafNode, YoutubeLeafNode, PassthroughLeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    URL = "url"
    IMAGE = "image"
    YOUTUBE = "youtube"
    PASSTHROUGH = "passthrough"


HTML_TEXT_TAGS = {
    TextType.BOLD: "strong",
    TextType.ITALIC: "em",
    TextType.CODE: "code",
    TextType.IMAGE: "img",
    TextType.URL: "a",
    TextType.PLAIN: "",
}


class TextNode:
    def __init__(
        self,
        text,
        text_type: TextType,
        url: str = "",
        props: dict[str, str] = {},
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        self.props = props

    def __eq__(self, value) -> bool:
        if not isinstance(value, TextNode):
            return False
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
            and self.props == value.props
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url}, {self.props})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:

    match text_node.text_type:

        case TextType.URL:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url} | text_node.props
            )

        case TextType.IMAGE:
            return ImageLeafNode(
                props={"src": text_node.url, "alt": text_node.text} | text_node.props
            )

        case TextType.YOUTUBE:
            return YoutubeLeafNode(props={"src": text_node.url} | text_node.props
            )
        
        case TextType.PASSTHROUGH:
            return PassthroughLeafNode(text_node.text)
    
    
    if isinstance(text_node.text, str):            
        return LeafNode(
            tag=HTML_TEXT_TAGS[text_node.text_type], value=text_node.text
        )
    elif isinstance(text_node.text, list):
        return ParentNode(
            tag=HTML_TEXT_TAGS[text_node.text_type], childen=[text_node_to_html_node(node) for node in text_node.text]
        )
    
    raise Exception("Error: Unexpected type")

def sort_delimiters(delimeters: list[str], text: str) -> list[str]:
    delimeters.sort(key=len, reverse=True)
    return_list = []
    for delim in delimeters:
        index = text.find(delim)
        if index < 0:
            continue
        text = text.replace(delim, '\n100')
        return_list.append((delim, index))
    return_list.sort(key= lambda item: item[1])
    for i in range(len(return_list)): return_list[i] = return_list[i][0]
    return return_list

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType, space_before_delim: bool = False, parse_substring: bool=True) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            continue

        if node.text_type != TextType.PLAIN or not isinstance(node.text, str):
            new_nodes.append(node)
            continue
        
        text = node.text

        while len(text) > 0:
            
            if space_before_delim:
                # If delim is at the start of the string
                if text[:len(delimiter)] == delimiter:
                    text_split = ['', text[len(delimiter):]]
                else:
                    text_split = text.split(' ' + delimiter, 1)
                    if len(text_split) > 1:
                        text_split[0] = text_split[0] + ' '
                                    
            else:
                text_split = text.split(delimiter, 1)
            
            if len(text_split) == 1:
                new_nodes.append(TextNode(text_split[0], TextType.PLAIN))
                break
            
            new_nodes.append(TextNode(text_split[0], TextType.PLAIN))
            
            delim_split = text_split[1].split(delimiter, 1)
            
            # If the delimiter isn't closed
            if len(delim_split) == 1:
                print(f'Warning: Delimiter "{delimiter}" is not closed. -> "{text}"')
                new_nodes.append(TextNode(delimiter + text_split[1], TextType.PLAIN))
                break
            
            substring = delim_split[0]
            
            if parse_substring:
                sub_text_nodes = text_to_textnodes(substring)
                
                # If there's nothing of note in the substring
                if len(sub_text_nodes) == 1 and sub_text_nodes[0].text_type == TextType.PLAIN:
                    substring = sub_text_nodes[0].text
                else:
                    substring = sub_text_nodes
            
            new_nodes.append(TextNode(substring, text_type))
            
            text = delim_split[1]

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str, str]]:
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)(?:\{([^}]*)\})?", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str, str]]:
    matches = re.findall(r"\[([^\]]*)\]\(([^)]+)\)(?:\{([^}]*)\})?", text)
    return matches

def extract_markdown_youtube(text: str) -> list[tuple[str, str, str]]:
    matches = re.findall(r"@\[([^\]]*)\]\(([^)]+)\)(?:\{([^}]*)\})?", text)
    return matches

def extract_markdown_passthrough(text: str) -> list[str]:
    #matches = re.findall(r"(?:^|[^\\]|\\\\)\{([^}]*)\}", text)
    #return matches
    
    results = []
    stack = []
    start = None
    i = 0
    while i < len(text):
        char = text[i]

        # Check if this "{" is escaped
        if char == '{':
            # Count backslashes before '{'
            backslashes = 0
            j = i - 1
            while j >= 0 and text[j] == '\\':
                backslashes += 1
                j -= 1

            if backslashes % 2 == 0:  # even number of "\" → not escaped
                if not stack:
                    start = i
                stack.append('{')

        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start is not None:
                    results.append(text[start + 1:i])  # exclude braces
                    start = None

        i += 1

    return results

def extract_special_properties(text: str) -> dict[str,str]:
    props = {}
    
    tag_pairs = re.split(r'(\w+\s*=\s*"[^"]*")', text)
    for tag_pair in tag_pairs:
        if tag_pair.strip() != '':
            tag_split = tag_pair.split("=", 1)
            props[tag_split[0]] = tag_split[1].replace('"', '')
    
    return props

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        imgs = extract_markdown_images(node.text)
        
        if len(imgs) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        
        for img in imgs:
            
            raw_string = f'![{img[0]}]({img[1]})'
            extra_tags = {}
            
            if img[2] != '':
                raw_string += '{' + img[2] + '}'                
                extra_tags = extract_special_properties(img[2])            
            
            split = text.split(raw_string, 1)
            
            img_node = TextNode(img[0], TextType.IMAGE, img[1], extra_tags)
            
            if split[1][:2] == "{}":
                split[1] = split[1][2:]
            
            # Check if wrapped in link syntax
            if '[' in split[0] and ']' in split[1]:
                img_html = text_node_to_html_node(img_node)
                text = split[0] + img_html.to_html() + split[1]
            else:
                new_nodes.append(TextNode(split[0], TextType.PLAIN))
                new_nodes.append(img_node)
                text = split[1]
        
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.PLAIN))
            
    return new_nodes
    
def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text = node.text
        urls = extract_markdown_links(text)

        if len(urls) == 0:
            new_nodes.append(node)
            continue
        
        for url in urls:
            raw_string = f'[{url[0]}]({url[1]})'
            extra_tags = {}
            
            if url[2] != '':
                raw_string += '{' + url[2] + '}'
                extra_tags = extract_special_properties(url[2])
                
            split = text.split(raw_string, 1)
            new_nodes.append(TextNode(split[0], TextType.PLAIN))
            
            text = text_to_textnodes(url[0])
            if len(text) == 1:
                text = text[0].text
            
            new_nodes.append(TextNode(text, TextType.URL, url[1], extra_tags))
            text = split[1]
        
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.PLAIN))
            
    return new_nodes

def split_nodes_passthrough(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        
        if not isinstance(node, TextNode):
            continue
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text = node.text.replace('{}', '')
        matches = extract_markdown_passthrough(text)
        
        for match in matches:            
            if len(match) == 0:
                continue
            
            split = text.split(match, 1)
            new_nodes.append(TextNode(split[0][:-1], TextType.PLAIN))
            new_nodes.append(TextNode(match, TextType.PASSTHROUGH))
            text = split[1][1:]
        
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.PLAIN))
    
    return new_nodes

def split_nodes_youtube(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:

        if not isinstance(node, TextNode):
            continue
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text = node.text
        
        videos = extract_markdown_youtube(text)

        if len(videos) == 0:
            new_nodes.append(node)
            continue

        for video in videos:
            
            raw_string = f'@[{video[0]}]({video[1]})'
            
            extra_tags = {}
            if video[2] != '':
                raw_string += '{' + video[2] + '}'
                extra_tags = extract_special_properties(video[2])
            
            split = text.split(raw_string, 1)
            new_nodes.append(TextNode(split[0], TextType.PLAIN))
            new_nodes.append(TextNode(video[0], TextType.YOUTUBE, video[1], extra_tags))
            text = split[1]
        
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.PLAIN))            

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:

    new_nodes = [TextNode(text, TextType.PLAIN)]
    
    delim_types = {
        '**': TextType.BOLD,
        '_' : TextType.ITALIC,
        '*' : TextType.ITALIC,
        '`' : TextType.CODE   
    }
    
    delimiters = sort_delimiters(list(delim_types.keys()), text)
    
    for delim in delimiters:
        text_type = delim_types[delim]
        
        new_nodes = split_nodes_delimiter(
            old_nodes = new_nodes, 
            delimiter = delim, 
            text_type = text_type, 
            space_before_delim = delim == '_', # Space before delim for '_' 
            parse_substring = delim != '`') # Parse substring for everything except '`'

    new_nodes = split_nodes_youtube(new_nodes)
    new_nodes = split_nodes_images(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    new_nodes = split_nodes_passthrough(new_nodes)

    return new_nodes
