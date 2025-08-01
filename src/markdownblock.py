import re
from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING1 = "heading 1"
    HEADING2 = "heading 2"
    HEADING3 = "heading 3"
    HEADING4 = "heading 4"
    HEADING5 = "heading 5"
    HEADING6 = "heading 6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CSV = "csv"
    CSV_WITH_HEADERS = "csv_with_headers"


HTML_BLOCK_TAGS = {
    BlockType.PARAGRAPH: "p",
    BlockType.CODE: "pre",
    BlockType.ORDERED_LIST: "ol",
    BlockType.UNORDERED_LIST: "ul",
    BlockType.QUOTE: "blockquote",
    BlockType.HEADING1: "h1",
    BlockType.HEADING2: "h2",
    BlockType.HEADING3: "h3",
    BlockType.HEADING4: "h4",
    BlockType.HEADING5: "h5",
    BlockType.HEADING6: "h6",
    BlockType.CSV: "table",
    BlockType.CSV_WITH_HEADERS: "table",
}


def markdown_to_blocks(markdown: str) -> list[str]:

    blocks = markdown.split("\n\n")

    for i in range(len(blocks) - 1, -1, -1):
        blocks[i] = blocks[i].strip()
        if len(blocks[i]) == 0:
            blocks.pop(i)

    return blocks


def block_to_block_type(block: str) -> BlockType:

    block = block.strip()

    if len(block) < 3:
        return BlockType.PARAGRAPH

    match block[0]:

        case "#":
            tag = block[:7]
            for i in range(len(tag)):
                if tag[i] == "#":
                    continue
                if tag[i] == " ":
                    match i:
                        case 1:
                            return BlockType.HEADING1
                        case 2:
                            return BlockType.HEADING2
                        case 3:
                            return BlockType.HEADING3
                        case 4:
                            return BlockType.HEADING4
                        case 5:
                            return BlockType.HEADING5
                        case 6:
                            return BlockType.HEADING6
                break

        case "`":
            if len(block) > 6 and block[:3] == "```" and block[-3:] == "```":
                return BlockType.CODE

        case ">":
            lines = block.split("\n")
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE

        case "-":
            lines = block.split("\n")
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

        case "1":
            lines = block.split("\n")
            for i in range(len(lines)):
                lines[i] = lines[i].strip()
                if len(lines[i]) == 0 or lines[i][:3] != f"{i + 1}. ":
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST

        case ":":

            if block[:3] == ":::" and block[-3:] == ":::":
                if block[3:6] == "csv":
                    if block[6:14] == "_headers":
                        return BlockType.CSV_WITH_HEADERS
                    else:
                        return BlockType.CSV

    return BlockType.PARAGRAPH


def block_to_html_node(block: str, block_type: BlockType) -> ParentNode:

    def code_to_html(block: str) -> ParentNode:
        trimmed_block = block[3:-3]

        if trimmed_block[0] == "\n":
            trimmed_block = trimmed_block[1:]

        return ParentNode(
            HTML_BLOCK_TAGS[BlockType.CODE],
            [text_node_to_html_node(TextNode(trimmed_block, TextType.CODE))],
        )

    def header_to_html(type: int, tag: str, block: str) -> ParentNode:
        text_nodes = text_to_textnodes(block[type:].strip())
        children_nodes = [text_node_to_html_node(node) for node in text_nodes]
        return ParentNode(tag, children_nodes)

    def quote_to_html(block: str) -> ParentNode:
        trimmed_block = re.sub("\n> ", "\n", block[2:].strip())
        text_nodes = text_to_textnodes(trimmed_block)
        leaf_nodes = [text_node_to_html_node(node) for node in text_nodes]
        return ParentNode(HTML_BLOCK_TAGS[BlockType.QUOTE], leaf_nodes)

    def list_to_html(tag_len: int, block: str) -> list[LeafNode]:
        lines = block.split("\n")
        text_nodes = [text_to_textnodes(line[tag_len:].strip()) for line in lines]
        children_nodes = []

        for nodes in text_nodes:
            leafs = ParentNode("li", [text_node_to_html_node(node) for node in nodes])
            children_nodes.append(leafs)

        return children_nodes

    def csv_to_html(has_headers: bool, block: str) -> ParentNode:
        if has_headers:
            trimmed_block = block[14:-3].strip()
        else:
            trimmed_block = block[6:-3].strip()

        table_node = ParentNode("table", [])
        cells = []
        cell = ""
        in_quotes = False

        for char in trimmed_block:

            if in_quotes:
                if char == '"':
                    in_quotes = False
                else:
                    cell += char
            else:
                if char in ",\n":
                    text_nodes = text_to_textnodes(cell)
                    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                    cells.append(ParentNode("td", html_nodes))
                    cell = ""

                    if char == "\n":
                        table_node.children.append(ParentNode("tr", cells))
                        cells = []

                elif char == '"':
                    in_quotes = True
                else:
                    cell += char

        text_nodes = text_to_textnodes(cell)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        cells.append(ParentNode("td", html_nodes))
        cell = ""

        table_node.children.append(ParentNode("tr", cells))

        if has_headers:
            for node in table_node.children[0].children:
                node.tag = "th"

        return table_node

    match block_type:

        case BlockType.CODE:
            return code_to_html(block)

        case BlockType.HEADING1:
            return header_to_html(1, HTML_BLOCK_TAGS[block_type], block)

        case BlockType.HEADING2:
            return header_to_html(2, HTML_BLOCK_TAGS[block_type], block)

        case BlockType.HEADING3:
            return header_to_html(3, HTML_BLOCK_TAGS[block_type], block)

        case BlockType.HEADING4:
            return header_to_html(4, HTML_BLOCK_TAGS[block_type], block)

        case BlockType.HEADING5:
            return header_to_html(5, HTML_BLOCK_TAGS[block_type], block)

        case BlockType.HEADING6:
            return header_to_html(6, HTML_BLOCK_TAGS[block_type], block)

        case BlockType.QUOTE:
            return quote_to_html(block)

        case BlockType.ORDERED_LIST:
            return ParentNode(HTML_BLOCK_TAGS[BlockType.ORDERED_LIST], list_to_html(3, block))  # type: ignore

        case BlockType.UNORDERED_LIST:
            return ParentNode(HTML_BLOCK_TAGS[BlockType.UNORDERED_LIST], list_to_html(2, block))  # type: ignore

        case BlockType.CSV:
            return csv_to_html(False, block)

        case BlockType.CSV_WITH_HEADERS:
            return csv_to_html(True, block)

        case __:
            text_nodes = text_to_textnodes(block.strip().replace("\n", " "))
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.PARAGRAPH], children_nodes)


def markdown_to_html_node(markdown: str) -> ParentNode:

    blocks = markdown_to_blocks(markdown)

    parent_html_node = ParentNode("div", [])

    for block in blocks:

        block_type = block_to_block_type(block)

        parent_html_node.children.append(block_to_html_node(block, block_type))

    return parent_html_node


def extract_title(parent_node: ParentNode) -> str:
    for block in parent_node.children:
        if block.tag == "h1":
            text = ""
            for child in block.children:
                text += child.value

            return text
    raise Exception("Error: Markdown file should have a main heading (Heading 1)")
