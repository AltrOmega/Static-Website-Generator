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

    blocks = markdown_to_bloks(markdown)
    
    content = blocks_to_html_node(blocks).to_html()
    title = extract_title_from_blocks(blocks)


    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    # Todo: make the filename be generated automaticaly based on template file name
    create_and_write_file(f"{dest_path}", template)
    

# Todo: start here
def generate_pages_recursive(content_source_path, template_path, dest_dir_path):
    if not os.path.exists(content_source_path):
        raise ValueError("Source path does not exist.")

    if not os.path.exists(dest_dir_path):
        raise ValueError("Destination path does not exist.")
    
    if os.path.isfile(content_source_path):
        raise ValueError("Source path must be a folder.")
    
    if os.path.isfile(dest_dir_path):
        raise ValueError("Destination path must be a folder.")
    
    path_list = os.listdir(content_source_path)
    for path in path_list:
        full_source = f"{content_source_path}/{path}"
        full_destination = f"{dest_dir_path}/{path}"

        name, ext = os.path.splitext(full_source)
        if os.path.isfile(full_source) and ext == '.md':
            file_destination = f"{dest_dir_path}/index.html"
            generate_page(full_source, template_path, file_destination)
            #shutil.copy(full_source, full_destination)
            continue
        
        os.mkdir(full_destination)
        #full_copy(full_source, full_destination)
        generate_pages_recursive(full_source, template_path, full_destination)


def main():
    shutil.rmtree('public')
    os.mkdir('public')
    full_copy('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')


if __name__ == '__main__':
    main()
