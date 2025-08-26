import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ImageLeafNode, YoutubeLeafNode, PassthroughLeafNode


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
        text: str,
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

        case __:
            return LeafNode(
                tag=HTML_TEXT_TAGS[text_node.text_type], value=text_node.text
            )


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            continue

        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        delim_len = len(delimiter)
        i = 0
        marker = 0
        while i < len(node.text):

            if "<img" in node.text[i : i + 4]:
                while node.text[i] != '>':
                    i += 1
            
            if node.text[i : i + delim_len] == delimiter:

                new_nodes.append(TextNode(node.text[marker:i], TextType.PLAIN))

                k = i + delim_len
                while node.text[k : k + delim_len] != delimiter:
                    if k + delim_len >= len(node.text):
                        raise Exception(
                            f'Error: Markdown tag "{delimiter}" not closed -> "{node.text[i:k]}"'
                        )
                    k += 1

                new_nodes.append(TextNode(node.text[i + delim_len : k], text_type))
                i = k + delim_len + 1
                marker = i - 1

            i += 1

        if marker < len(node.text):
            new_nodes.append(
                TextNode(node.text[marker : len(node.text)], TextType.PLAIN)
            )

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

def split_nodes_links_and_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text = node.text
        
        imgs = extract_markdown_images(node.text)
        
        for img in imgs:
            raw_string = f'![{img[0]}]({img[1]})'
            extra_tags = {}
            
            if img[2] != '':
                raw_string += '{' + img[2] + '}'                
                extra_tags = extract_special_properties(img[2])            
            
            text_node = TextNode(img[0], TextType.IMAGE, img[1], extra_tags)
            html_node = text_node_to_html_node(text_node)
            text = text.replace(raw_string, html_node.to_html())
        
        urls = extract_markdown_links(text)

        if len(urls) == 0 and len(imgs) == 0:
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
            new_nodes.append(TextNode(url[0], TextType.URL, url[1], extra_tags))
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

    new_nodes = split_nodes_youtube(new_nodes)
    new_nodes = split_nodes_links_and_images(new_nodes)
    new_nodes = split_nodes_passthrough(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

    return new_nodes
