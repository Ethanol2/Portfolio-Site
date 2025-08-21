import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ImageLeafNode, YoutubeLeafNode, PassthroughLeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bolt"
    ITALIC = "italic"
    CODE = "code"
    URL = "url"
    IMAGE = "image"
    YOUTUBE = "youtube"
    PASSTHROUGH = "passthrough"


HTML_TEXT_TAGS = {
    TextType.BOLD: "b",
    TextType.ITALIC: "i",
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
        extra_tags: dict[str, str] = {},
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        self.extra_tags = extra_tags

    def __eq__(self, value) -> bool:
        if not isinstance(value, TextNode):
            return False
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
            and self.extra_tags == value.extra_tags
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url}, {self.extra_tags})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:

    match text_node.text_type:

        case TextType.URL:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )

        case TextType.IMAGE:
            return ImageLeafNode(
                props={"src": text_node.url, "alt": text_node.text}
                | text_node.extra_tags
            )

        case TextType.YOUTUBE:
            return YoutubeLeafNode(props={"src": text_node.url})
        
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

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_youtube(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"@\[(.*?)\]\((.*?)\)", text)
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

def split_nodes_links_and_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        imgs = extract_markdown_images(node.text)
        
        for img in imgs:
            raw_string = f'![{img[0]}]({img[1]})'
            extra_tags = {}
            
            if img[2] != '':
                raw_string += '{' + img[2] + '}'
                
                tag_pairs = re.split(r'(\w+\s*=\s*"[^"]*")', img[2])
                for tag_pair in tag_pairs:
                    if tag_pair.strip() != '':
                        tag_split = tag_pair.split("=", 1)
                        extra_tags[tag_split[0]] = tag_split[1].replace('"', '')
            
            
            text_node = TextNode(img[0], TextType.IMAGE, img[1], extra_tags)
            html_node = text_node_to_html_node(text_node)
            node.text = node.text.replace(raw_string, html_node.to_html())
        
        urls = extract_markdown_links(node.text)

        if len(urls) == 0:
            new_nodes.append(node)
            continue

        last_index = 0
        for url in urls:
            txt_len = len(url[0]) + len(url[1]) + 4
            index = node.text.find(f"[{url[0]}]", last_index)

            new_nodes.append(TextNode(node.text[last_index:index], TextType.PLAIN))
            new_nodes.append(TextNode(url[0], TextType.URL, url[1]))

            last_index = index + txt_len

        if last_index < len(node.text):
            new_nodes.append(
                TextNode(node.text[last_index : len(node.text)], TextType.PLAIN)
            )

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

        videos = extract_markdown_youtube(node.text)

        if len(videos) == 0:
            new_nodes.append(node)
            continue

        last_index = 0
        for video in videos:
            txt_len = len(video[0]) + len(video[1]) + 5
            index = node.text.find(f"@[{video[0]}]", last_index)

            new_nodes.append(TextNode(node.text[last_index:index], TextType.PLAIN))
            new_nodes.append(TextNode(video[0], TextType.YOUTUBE, video[1]))

            last_index = index + txt_len

        if last_index < len(node.text):
            new_nodes.append(
                TextNode(node.text[last_index : len(node.text)], TextType.PLAIN)
            )

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
