import os
import shutil
import sys

from markdownblock import markdown_to_html_node_and_metadata, extract_title, header_block_to_html
from htmlnode import LeafNode
from templatelibrary import TemplateLibrary
from yamlblock import yaml_to_html_node

def main():

    base_path = ""

    # Get base path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    # Create paths
    static_path = os.path.join(base_path, "static/")
    content_path = os.path.join(base_path, "content/")
    data_path = os.path.join(base_path, "data/")
    templates_path = os.path.join(base_path, "templates/")

    # To be removed
    header_template_path = os.path.join(base_path, "templates/header_template.html")

    public_path = "docs/"

    # Check paths exist
    if not os.path.exists(static_path):
        raise Exception(f'The static folder doesn\'t exist. "{static_path}"')
    if not os.path.exists(content_path):
        raise Exception(f'The content folder doesn\'t exist. "{content_path}"')
    if not os.path.exists(data_path):
        raise Exception(f'The data folder doesn\'t exist. "{data_path}"')
    if not os.path.exists(templates_path):
        raise Exception(f'The HTML templates folder is missing. "{templates_path}"')

    # Clear the public folder
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    os.mkdir(public_path)

    # Find Templates
    templates= TemplateLibrary(templates_path, base_path)

    # Populate public folder
    header_html = generate_header(data_path, header_template_path)
    copy_dir_to_dir(static_path, public_path)
    js_html = generate_js_html(public_path)
    generate_pages_recursive(content_path, templates, public_path, header_html, js_html)

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


def generate_header(content_path: str, header_template_path: str) -> str:

    header_path = os.path.join(content_path, "header.yaml")
    if not os.path.exists(header_path):
        raise Exception(f'The header.md is missing in the content folder. "{content_path}"')

    with open(header_path) as f:
        file_contents = f.read()
        f.close()
    
    return yaml_to_html_node(file_contents).to_html()
    
def copy_dir_to_dir(source: str, destination: str):

    for item in os.listdir(source):
        src_joined_path = os.path.join(source, item)
        tgt_joined_path = os.path.join(destination, item)

        if os.path.isfile(src_joined_path):
            shutil.copy(src_joined_path, tgt_joined_path)
        else:
            os.mkdir(tgt_joined_path)
            copy_dir_to_dir(src_joined_path, tgt_joined_path)


def generate_pages_recursive(dir_path_content: str, templates: TemplateLibrary, dest_dir_path: str, header_html: str, js_html: str):

    for item in os.listdir(dir_path_content):

        path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(path):
            generate_pages_recursive(path, templates, dest_path, header_html, js_html)
        elif os.path.isfile(path) and ".md" in path:
            generate_page(templates, path, dest_path[:-3] + ".html", header_html, js_html)


def generate_page(templates: TemplateLibrary, src_path: str, dest_path: str, header_html: str, js_html: str):

    with open(src_path) as f:
        file_contents = f.read()
        f.close()

    html_node, metadata = markdown_to_html_node_and_metadata(file_contents)
    
    if "title" in metadata.keys():
        title = metadata["title"]
    else:
        title = extract_title(html_node)
        
    template_name = "default"
    if "layout" in metadata.keys():
        template_name = metadata["layout"]
        
    template_contents = templates.get_template(template_name)

    print(f'Generating page from {src_path} to {dest_path} using the "{template_name}" template')
    
    template_contents = template_contents.replace("{{ Header }}", header_html)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_node.to_html())
    template_contents = template_contents.replace("{{ JavaScript }}", js_html)

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
