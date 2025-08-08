import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ImageLeafNode, YoutubeLeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bolt"
    ITALIC = "italic"
    CODE = "code"
    URL = "url"
    IMAGE = "image"
    YOUTUBE = "youtube"


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


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:

        if not isinstance(node, TextNode):
            continue
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        imgs = extract_markdown_images(node.text)

        if len(imgs) == 0:
            new_nodes.append(node)
            continue

        last_index = 0
        for image in imgs:

            has_extra_tags = image[2] != ""
            extra_tags = {}

            if has_extra_tags:
                tag_pairs = image[2].split(",")
                for tag_pair in tag_pairs:
                    tag_split = tag_pair.split("=")
                    extra_tags[tag_split[0]] = tag_split[1]

            txt_len = (
                len(image[0])
                + len(image[1])
                + (len(image[2]) + 7 if has_extra_tags else 5)
            )
            index = node.text.find(f"![{image[0]}]", last_index)

            new_nodes.append(TextNode(node.text[last_index:index], TextType.PLAIN))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1], extra_tags))

            last_index = index + txt_len

        if last_index < len(node.text):
            new_nodes.append(
                TextNode(node.text[last_index : len(node.text)], TextType.PLAIN)
            )

    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:

        if not isinstance(node, TextNode):
            continue
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

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

    new_nodes = split_nodes_images([TextNode(text, TextType.PLAIN)])
    new_nodes = split_nodes_youtube(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

    return new_nodes
