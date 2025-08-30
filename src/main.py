import os
import shutil
import sys

from markdownblock import markdown_to_html_and_metadata, ref_js_in_html
from templatelibrary import TemplateLibrary
from yamlblock import yaml_to_html_node

JS = "javascript"
HEADER = "header"
FOOTER = "footer"

def main():

    base_path = "/"

    # Get base path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    # Create paths
    static_path = "static/"
    content_path = "content/"
    data_path = "data/"
    templates_path = "templates/"

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
    copy_dir_to_dir(static_path, public_path)
    
    # Generate Insert HTML
    inserts = {}
    inserts[HEADER] = generate_html_from_yaml(data_path, "header.yaml")
    inserts[FOOTER] = generate_html_from_yaml(data_path, "footer.yaml")
    inserts[JS] = generate_js_html(public_path, base_path)
    
    # Generate HTML
    generate_pages_recursive(content_path, templates, public_path, inserts)

def generate_js_html(content_path: str, base_path: str) -> str:

    html = ""
    for item in os.listdir(content_path):
        path = os.path.join(content_path, item)
        if os.path.isfile(path):
            if '.js' in item:
                html += '\n' + ref_js_in_html(base_path + item)
        else:
            html += generate_js_html(path, base_path)
    
    return html.strip()

def generate_html_from_yaml(content_path: str, file_name: str) -> str:

    file_path = os.path.join(content_path, file_name)
    if not os.path.exists(file_path):
        raise Exception(f'The file "{file_name}" is missing in the content folder. "{content_path}"')

    with open(file_path) as f:
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


def generate_pages_recursive(dir_path_content: str, templates: TemplateLibrary, dest_dir_path: str, html_inserts: dict[str, str]):

    for item in os.listdir(dir_path_content):

        path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(path):
            generate_pages_recursive(path, templates, dest_path, html_inserts)
        elif os.path.isfile(path) and ".md" in path:
            generate_page(templates, path, dest_path[:-3] + ".html", html_inserts)


def generate_page(templates: TemplateLibrary, src_path: str, dest_path: str, html_inserts: dict[str, str]):

    with open(src_path) as f:
        file_contents = f.read()
        f.close()

    try:
        html, metadata = markdown_to_html_and_metadata(file_contents)
    except Exception as e:
        print(f'The file at "{src_path}" caused an exception to occur:\n{e}')
        return
    
    template_name = "default"
    if "layout" in metadata.keys():
        template_name = metadata["layout"].lower()
        
    template_contents = templates.get_template(template_name)

    print(f'Generating page from {src_path} to {dest_path} using the "{template_name}" template')
    
    template_contents = template_contents.replace("{{ Header }}", html_inserts[HEADER])
    template_contents = template_contents.replace("{{ Title }}", metadata["title"])
    template_contents = template_contents.replace("{{ Content }}", html)
    template_contents = template_contents.replace("{{ JavaScript }}", html_inserts[JS])
    template_contents = template_contents.replace("{{ Footer }}", html_inserts[FOOTER])
    
    # template_contents = template_contents.replace('href="/', f'href="{base_path}')
    # template_contents = template_contents.replace('src="/', f'src="{base_path}')


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
