import os
import shutil
from textnode import TextNode, TextType
from md_handle import *


def full_copy(source, destination):
    if not os.path.exists(source):
        raise ValueError("Source path does not exist.")

    if not os.path.exists(destination):
        raise ValueError("Destination path does not exist.")
    
    if os.path.isfile(source):
        raise ValueError("Source path must be a folder.")
    
    if os.path.isfile(destination):
        raise ValueError("Destination path must be a folder.")
    
    path_list = os.listdir(source)
    for path in path_list:
        full_source = f"{source}/{path}"
        full_destination = f"{destination}/{path}"
        if os.path.isfile(full_source):
            shutil.copy(full_source, full_destination)
            continue
        
        os.mkdir(full_destination)
        full_copy(full_source, full_destination)



def read_file_as_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {e}"

def create_and_write_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file_as_string(from_path)
    template = read_file_as_string(template_path)
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    # Todo: make the filename be generated automaticaly based on template file name
    create_and_write_file(f"{dest_path}/index.html", template)
    




DEFAULT_SOURCE = 'static'
DEFAULT_DESTINATION = 'public'
DEFAULT_TEMPLATE = 'template.html'
DEFAULT_MARKDOWN = 'content/index.md'
def main():
    source = DEFAULT_SOURCE
    destination = DEFAULT_DESTINATION
    template = DEFAULT_TEMPLATE

    shutil.rmtree(destination)
    os.mkdir(destination)

    full_copy(source, destination)
    generate_page(DEFAULT_MARKDOWN, template, destination)


if __name__ == '__main__':
    main()
