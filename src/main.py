import os
import shutil
import sys

from markdownblock import markdown_to_html_node, extract_title, header_block_to_html
from htmlnode import LeafNode

def main():

    base_path = "/"

    # Get base path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    # Create paths
    static_path = "static/"
    content_path = "content/"
    template_path = "template.html"
    header_template_path = "header_template.html"

    public_path = "docs/"

    # Check paths exist
    if not os.path.exists(static_path):
        raise Exception(f'The static folder doesn\'t exist. "{static_path}"')
    if not os.path.exists(content_path):
        raise Exception(f'The content folder doesn\'t exist. "{content_path}"')
    if not os.path.exists(template_path):
        raise Exception(f'The HTML template is missing. "{template_path}"')
    if not os.path.exists(header_template_path):
        raise Exception(f'The header HTML template is missing. "{header_template_path}"')

    # Clear the public folder
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    os.mkdir(public_path)

    # Populate public folder
    header_html, title_suffix = generate_header(content_path, header_template_path)
    copy_dir_to_dir(static_path, public_path)
    js_html = generate_js_html(public_path)
    generate_pages_recursive(base_path, content_path, template_path, public_path, header_html, js_html, title_suffix)

def generate_js_html(content_path: str) -> str:

    html = ""
    for item in os.listdir(content_path):
        path = os.path.join(content_path, item)
        if os.path.isfile(path):
            if '.js' in item:
                html += '\n' + LeafNode("script", "", {"src":item}).to_html()
        else:
            html += generate_js_html(path)
    
    return html.strip()


def generate_header(content_path: str, header_template_path: str) -> tuple[str, str]:

    header_path = os.path.join(content_path, "_header.md")
    if not os.path.exists(header_path):
        raise Exception(f'The header.md is missing in the content folder. "{content_path}"')

    with open(header_path) as f:
        file_contents = f.read()
        f.close()
    
    blocks = file_contents.split("\n\n")

    title_content = header_block_to_html(blocks[0])
    nav_links = header_block_to_html(blocks[1])
    contact_links = header_block_to_html(blocks[2])

    title_suffix = " | "
    for node in title_content.children:
        if node.tag == "":
            title_suffix += node.value

    for node in contact_links.children:
        node.props["target"] = "_blank"

    with open(header_template_path) as f:
        template_contents = f.read()
        f.close()
    
    template_contents = template_contents.replace("{{ Title }}", title_content.to_html())
    template_contents = template_contents.replace("{{ Nav Links }}", nav_links.to_html())
    template_contents = template_contents.replace("{{ Contact Links }}", contact_links.to_html())

    return template_contents, title_suffix

def copy_dir_to_dir(source: str, destination: str):

    for item in os.listdir(source):
        src_joined_path = os.path.join(source, item)
        tgt_joined_path = os.path.join(destination, item)

        if os.path.isfile(src_joined_path):
            shutil.copy(src_joined_path, tgt_joined_path)
        else:
            os.mkdir(tgt_joined_path)
            copy_dir_to_dir(src_joined_path, tgt_joined_path)


def generate_pages_recursive(
    base_path: str, dir_path_content: str, template_path: str, dest_dir_path: str, header_html: str, js_html: str, title_suffix: str
):

    for item in os.listdir(dir_path_content):

        path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(path):
            generate_pages_recursive(base_path, path, template_path, dest_path, header_html, js_html, title_suffix)
        elif os.path.isfile(path) and ".md" in path:
            generate_page(base_path, path, template_path, dest_path[:-3] + ".html", header_html, js_html, title_suffix)


def generate_page(base_path: str, src_path: str, template_path: str, dest_path: str, header_html: str, js_html: str, title_suffix):

    if os.path.basename(src_path)[0] == '_':
        return

    print(f"Generating page from {src_path} to {dest_path} using {template_path}")

    if src_path is None or template_path is None or dest_path is None:
        raise Exception("Error: All paths must have a value")

    with open(src_path) as f:
        file_contents = f.read()
        f.close()

    html_node = markdown_to_html_node(file_contents)
    title = extract_title(html_node) + title_suffix

    with open(template_path) as f:
        template_contents = f.read()
        f.close()

    template_contents = template_contents.replace("{{ Header }}", header_html)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_node.to_html())
    template_contents = template_contents.replace("{{ JavaScript }}", js_html)
    template_contents = template_contents.replace('href="/', f'href="{base_path}')
    template_contents = template_contents.replace('src="/', f'src="{base_path}')

    dest_path_split = dest_path.split("/")
    if not os.path.isfile(dest_path_split[0]):

        if dest_path_split[0] == ".":
            dest_path_split = dest_path_split[1:]

        path = ""
        for i in range(len(dest_path_split) - 1):
            path = os.path.join(path, dest_path_split[i])
            if not os.path.exists(path):
                os.mkdir(path)

    with open(dest_path, "w+") as f:
        f.write(template_contents)
        f.close()


main()
