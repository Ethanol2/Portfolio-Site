import re
from enum import Enum
from htmlnode import ParentNode, LeafNode, HorizontalLineLeafNode
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
    CSV_WITH_HEADERS = "csv_with_headers",
    HORIZONTAL_LINE = "horizontal_line",
    CUSTOM = "custom",
    NONE = "empty"


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
    BlockType.HORIZONTAL_LINE: "hr",
    BlockType.CUSTOM: "div"
}

# Returns the block, the type and the remainder
def markdown_to_block_and_type(markdown_lines: list[str]) -> tuple[str, BlockType, list[str]]:
    
    if markdown_lines[0].strip() == '':
        return '', BlockType.NONE, markdown_lines[1:] 
    
    if len(markdown_lines) == 1: 
        if len(markdown_lines[0]) < 3:
            return markdown_lines[0], BlockType.PARAGRAPH, []

    lines = markdown_lines
    lines[0] = lines[0].strip()
    
    match lines[0][0]:

        case "#":
            tag = lines[0][:7]
            
            for i in range(len(tag)):
                if tag[i] == "#":
                    continue
                if tag[i] == " ":
                    match i:
                        case 1:
                            return lines[0], BlockType.HEADING1, lines[1:]
                        case 2:
                            return lines[0], BlockType.HEADING2, lines[1:]
                        case 3:
                            return lines[0], BlockType.HEADING3, lines[1:]
                        case 4:
                            return lines[0], BlockType.HEADING4, lines[1:]
                        case 5:
                            return lines[0], BlockType.HEADING5, lines[1:]
                        case 6:
                            return lines[0], BlockType.HEADING6, lines[1:]
                break

        case "`":
            if lines[0] == '```':
                code = ""
                i = 1
                while i < len(lines) and lines[i] != '```':
                    code += lines[i] + '\n'
                    i += 1
                
                if i >= len(lines):
                    raise Exception('Error: Code marker "```" never closed')
                                
                return code, BlockType.CODE, lines[i + 1:]

        case ">":
                        
            quote = ""
            i = 0
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[0] != ">":
                    break
                quote += '\n' + line
                i += 1
            
            if len(quote) > 0:
                return quote, BlockType.QUOTE, lines[i:]

        case "-":
            if lines[0] == "---":
                return lines[0], BlockType.HORIZONTAL_LINE, lines[1:]
            
            list = ""
            i = 0
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[:2] != "- ":
                    break
                list += '\n' + line
                i += 1
            
            if len(list) > 0:
                return list.strip(), BlockType.UNORDERED_LIST, lines[i:]

        case "1":
            if lines[0][:2] == '1.':
                
                list = ""
                i = 0
                for i in range(len(lines)):
                    lines[i] = lines[i].strip()
                    if len(lines[i]) == 0 or lines[i][:3] != f"{i + 1}. ":
                        break
                    list += '\n' + lines[i]
                        
                if len(list) > 0:
                    return list.strip(), BlockType.ORDERED_LIST, lines[i + 1:]

        case ":":
            
            if lines[0][:3] == ":::":
                
                nest = 0
                contents = ""
                i = 0
                for line in lines:
                    line = line.strip()
                    if line == ':::':
                        nest -= 1
                        if nest == 0:
                            contents += '\n' + line
                            i += 1
                            break
                    elif line[:4] == '::: ':
                        nest += 1
                    
                    contents += '\n' + line
                    i += 1
            
                if nest > 0:                    
                    raise Exception("Error: Custom marker ':::' not closed")
                
                contents = contents.strip()
                
                if contents[4:7] == "csv":
                    if contents[7:15] == "_headers":
                        return contents, BlockType.CSV_WITH_HEADERS, lines[i:]
                    else:
                        return contents, BlockType.CSV, lines[i:]
                else:
                    return contents, BlockType.CUSTOM, lines[i:]

    
    contents = ""
    i = 0
    while i < len(lines) and lines[i] != '':
        contents += '\n' + lines[i]
        i += 1
    
    return contents, BlockType.PARAGRAPH, lines[i:] if i + 1 < len(lines) else []

def block_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    
    def code_to_html(block: str) -> ParentNode:
        
        return ParentNode(
            HTML_BLOCK_TAGS[BlockType.CODE],
            [text_node_to_html_node(TextNode(block, TextType.CODE))],
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

        def markdown_cell_to_html(cell: str) -> list:
            cell_node = markdown_to_html(cell)
            return cell_node.children

        def basic_cell_to_html(cell: str) -> list:
            cell = cell.replace("\n", "<br>")
            text_nodes = text_to_textnodes(cell)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return html_nodes

        if has_headers:
            trimmed_block = block[15:-3].strip()
        else:
            trimmed_block = block[7:-3].strip()

        table_node = ParentNode("table", [])
        cells = []
        cell = ""
        in_quotes = False
        full_markdown = False

        for char in trimmed_block:

            if in_quotes:
                if char == '"':
                    in_quotes = False
                else:
                    cell += char
            else:
                if char in ",\n":

                    if full_markdown:
                        cell_nodes = markdown_cell_to_html(cell)
                        full_markdown = False
                    else:
                        cell_nodes = basic_cell_to_html(cell)

                    cells.append(ParentNode("td", cell_nodes))
                    cell = ""

                    if char == "\n":
                        table_node.children.append(ParentNode("tr", cells))
                        cells = []

                elif char == '"':
                    in_quotes = True
                    cell = ""
                    full_markdown = True
                else:
                    cell += char

        if full_markdown:
            cell_nodes = markdown_cell_to_html(cell)
        else:
            cell_nodes = basic_cell_to_html(cell)

        cells.append(ParentNode("td", cell_nodes))
        cell = ""

        table_node.children.append(ParentNode("tr", cells))

        if has_headers:
            header_row = ParentNode("thead", [table_node.children[0]])
            
            for node in header_row.children[0].children:
                node.tag = "th"
                
            table_node.children[0] = header_row

        return table_node

    def custom_to_html(block: str) -> ParentNode:
        split = block.split('\n', 1)
        custom_class = split[0][3:].strip()
        block = split[1].strip()[:-3].strip()
            
        custom_node = markdown_to_html(block)
        custom_node.props = {"class":custom_class}

        return custom_node

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
        
        case BlockType.CUSTOM:
            return custom_to_html(block)

        case __:
            text_nodes = text_to_textnodes(block.strip().replace("\n", " "))
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.PARAGRAPH], children_nodes)

def markdown_to_html_and_metadata(markdown: str) -> tuple[str, dict[str,str]]:
    
    metadata, markdown = extract_metadata(markdown)
    blocks = markdown_to_html(markdown)
    html = blocks.to_html()
    
    if "title" not in metadata.keys():
        metadata["title"] = extract_title(blocks)

    return html, metadata


def markdown_to_html(markdown: str) -> ParentNode:

    parent_html_node = ParentNode("div", [])
    remainder = markdown.splitlines()
    
    while len(remainder) > 0:
        
        block, block_type, remainder = markdown_to_block_and_type(remainder)
        if block_type == BlockType.HORIZONTAL_LINE:
            parent_html_node.children.append(HorizontalLineLeafNode())
        elif block_type == BlockType.NONE:
            continue
        elif len(block) > 0:
            parent_html_node.children.append(block_to_html_node(block, block_type))

    return parent_html_node


def extract_title(parent_node: ParentNode) -> str:
    for block in parent_node.children:
        if block.tag == "h1":
            text = ""
            for child in block.children:
                text += child.value

            return text
    print("Warning: Markdown content has no title included in its metadate, nor a main heading (h1). Page title will be blank")
    return ''

def extract_metadata(markdown_file: str) -> tuple[dict[str, str], str]:
    
    if len(markdown_file) == 0:
        return {}, markdown_file

    raw_text = markdown_file.strip()
    
    # No meta data syntax at the top of the file
    if raw_text[:4] != '---\n':
        return {}, markdown_file
    raw_text = raw_text[4:]
    
    props = {}
    
    line_split = []
    while '---' not in line_split:
        
        line_split = raw_text.split('\n', 1)
        
        if len(line_split) < 2:
            raise Exception("Error: Metadata not closed")
        
        if line_split[0] != '---':
            values = line_split[0].split(':', 1)
            props[values[0].strip().lower()] = values[1].strip()

        raw_text = line_split[1]
        
    return props, raw_text

def ref_js_in_html(js_file: str) -> str:
    return LeafNode("script", "", {"src":js_file}).to_html()