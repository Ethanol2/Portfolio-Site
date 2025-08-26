import re
from enum import Enum
from typing import Any
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
    TABLE = "table"
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
    BlockType.TABLE: "table",
    BlockType.CSV: "table",
    BlockType.CSV_WITH_HEADERS: "table",
    BlockType.HORIZONTAL_LINE: "hr",
    BlockType.CUSTOM: "div"
}

# Returns the block, the type and the remainder
def markdown_to_block_and_type(markdown_lines: list[str]) -> tuple[Any, BlockType, list[str]]:
    
    def is_unordered_list(line: str) -> bool:
        if line == "---":
            return False
        return True
        
    def is_ordered_list(line: str) -> tuple[bool, Any]:
        num_chars = line.split('.', 1)
        n = int(num_chars[0]) if num_chars[0].isdecimal() else None 
        
        return n is not None and line.find(f'{n}. ') == 0, n
    
    def get_indent_level(line: str) -> int:
        line = line.replace('    ', '\t')
        return line.count('\t')
    
    def parse_unordered_list(lines: list[str], indent_lvl: int) -> tuple[list, int]:        
        md_list = []
        i = 0
        while i < len(lines):
            
            line = lines[i]
            line_indent = get_indent_level(line)
            line = line.strip()
            
            if line_indent - 1 == indent_lvl:
                is_ol, n = is_ordered_list(line)
                if is_ol:
                    sub_list, length = parse_ordered_list(lines[i:], n, line_indent)
                    sub_list.insert(0, BlockType.ORDERED_LIST)
                    md_list.append(sub_list)
                    i += length
                elif is_unordered_list(line):
                    sub_list, length = parse_unordered_list(lines[i:], line_indent)
                    sub_list.insert(0, BlockType.UNORDERED_LIST)
                    md_list.append(sub_list)
                    i += length
                continue
            elif line_indent != indent_lvl:
                break
            
            if len(line) == 0 or line[:2] != "- ":
                break
            md_list.append(line[2:])
            i += 1
        
        return md_list, i
    
    def parse_ordered_list(lines: list[str], start_num: int, indent_lvl: int) -> tuple[list, int]:
        md_list = []
        md_list.append(start_num)
        
        i = 0
        current_num = start_num
        while i < len(lines):
            line = lines[i]
            line_indent = get_indent_level(line)
            line = line.strip()
            if line_indent - 1 == indent_lvl:
                is_ol, n = is_ordered_list(line)
                if is_ol:
                    sub_list, length = parse_ordered_list(lines[i:], n, line_indent)
                    sub_list.insert(0, BlockType.ORDERED_LIST)
                    md_list.append(sub_list)
                    i += length
                elif is_unordered_list(line):
                    sub_list, length = parse_unordered_list(lines[i:], line_indent)
                    sub_list.insert(0, BlockType.UNORDERED_LIST)
                    md_list.append(sub_list)
                    i += length
                continue
            elif line_indent != indent_lvl:
                break
                    
            tag_len = len(f'{start_num}') + 2
            if len(line) == 0 or line[:tag_len] != f"{current_num}. ":
                break
            
            md_list.append(line[tag_len:])
            i += 1
            current_num += 1
                    
        return md_list, i
    
    if markdown_lines[0].strip() == '':
        return '', BlockType.NONE, markdown_lines[1:] 

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
                                
                return code.strip(), BlockType.CODE, lines[i + 1:]

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
                return quote.strip(), BlockType.QUOTE, lines[i:]

        case "-":            
            if is_unordered_list(lines[0]):
                ul_list, remainder = parse_unordered_list(lines, 0)
                return ul_list, BlockType.UNORDERED_LIST, lines[remainder:]
            
            return lines[0], BlockType.HORIZONTAL_LINE, lines[1:]

        case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0":
            is_ol, n = is_ordered_list(lines[0])
            if is_ol:                
                ol_list, remainder = parse_ordered_list(lines, n, 0)
                return ol_list, BlockType.ORDERED_LIST, lines[remainder:]

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

        case "|":
            if lines[0][-1] == '|':
                
                format_line = lines[1]
                if format_line[0] == '|' and format_line[-1] == '|':
                    format_cells = format_line[1:-1].split('|')
                    good_format = True
                    for cell in format_cells:
                        format_cells= format_cells and cell.count('-') > 0
                    
                    if good_format:                        
                        i = 0
                        table = []
                        while i < len(lines):
                            if lines[i][0] == '|' and lines[i][-1] == '|':
                                table.append(lines[i])
                            else:
                                i -= 1
                                break
                            i += 1
                            
                        return table, BlockType.TABLE, lines[i:]
    
    contents = ""
    i = 0
    while i < len(lines) and lines[i] != '':
        contents += '\n' + lines[i]
        i += 1
    
    return contents.strip(), BlockType.PARAGRAPH, lines[i:] if i + 1 < len(lines) else []

def block_to_html_node(block, block_type: BlockType) -> ParentNode:
    
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

    def list_to_html(block: list) -> list[LeafNode]:
        text_nodes = []
        
        for line in block:
            if isinstance(line, str):
                text_nodes.append(text_to_textnodes(line))
            elif isinstance(line, list):
                block_type = line.pop(0)
                                
                if isinstance(block_type, BlockType):
                    text_nodes.append(block_to_html_node(line, block_type))                
        
        children_nodes = []

        for nodes in text_nodes:
            leafs = ParentNode("li", [])
            if isinstance(nodes, ParentNode):
                children_nodes[-1].children.append(nodes)
            else:
                leafs.children = [text_node_to_html_node(node) for node in nodes]
                children_nodes.append(leafs)                

        return children_nodes

    def csv_to_html(has_headers: bool, block: str) -> ParentNode:

        def markdown_cell_to_html(cell: str) -> list:
            cell_node = markdown_to_html_node(cell)
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

    def table_to_html(block: list[str]) -> ParentNode:
        table_node = ParentNode(HTML_BLOCK_TAGS[block_type], [])
        
        # Header
        headers_node = ParentNode("thead", [ParentNode("tr", [])], {})
        headers = block.pop(0)[1:-1].split('|')
        for header in headers:
            text_nodes = text_to_textnodes(header.strip())
            headers_node.children[0].children.append(ParentNode("th", [text_node_to_html_node(node) for node in text_nodes]))
        table_node.children.append(headers_node)
        
        # Formatting
        formating = []
        format_row = block.pop(0)[1:-1].split('|')
        for cell in format_row:
            cell = cell.strip()
            if cell[-1] == ':':
                if cell[0] == ':':
                    alignment = "center"
                else:
                    alignment = "right"
            else:
                alignment = "left"
            
            formating.append(alignment)
        
        # Body
        body_node = ParentNode("tbody", [])
        for row in block:
            cells = row[1:-1].split('|')
            row_node = ParentNode("tr", [])
            for i in range(len(cells)):
                text_nodes = text_to_textnodes(cells[i].strip())
                row_node.children.append(ParentNode("td", [text_node_to_html_node(node) for node in text_nodes], {"align":formating[i]}))
            body_node.children.append(row_node)
        table_node.children.append(body_node)
        
        return table_node
    
    def custom_to_html(block: str) -> ParentNode:
        split = block.split('\n', 1)
        custom_class = split[0][3:].strip()
        block = split[1].strip()[:-3].strip()
            
        custom_node = markdown_to_html_node(block)
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
            return ParentNode(HTML_BLOCK_TAGS[BlockType.ORDERED_LIST], list_to_html(block[1:]), {"start":block[0]})  # type: ignore

        case BlockType.UNORDERED_LIST:
            return ParentNode(HTML_BLOCK_TAGS[BlockType.UNORDERED_LIST], list_to_html(block))  # type: ignore

        case BlockType.TABLE:
            return table_to_html(block)
        
        case BlockType.CSV:
            return csv_to_html(False, block)

        case BlockType.CSV_WITH_HEADERS:
            return csv_to_html(True, block)
        
        case BlockType.CUSTOM:
            return custom_to_html(block)

        case __:
            text_nodes = text_to_textnodes(block.replace("\n", " "))
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.PARAGRAPH], children_nodes)

def markdown_to_html_and_metadata(markdown: str) -> tuple[str, dict[str,str]]:
    
    metadata, markdown = extract_metadata(markdown)
    blocks = markdown_to_html_node(markdown)
    html = blocks.to_html()
    
    if "title" not in metadata.keys():
        metadata["title"] = extract_title(blocks)

    return html, metadata


def markdown_to_html_node(markdown: str) -> ParentNode:

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