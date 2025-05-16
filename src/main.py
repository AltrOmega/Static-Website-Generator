from textnode import TextNode, TextType
import os
import shutil

def full_copy(source, destination):
    shutil.rmtree(destination)
    os.mkdir(destination)
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




SOURCE = 'static'
DESTINATION = 'public'
def main():
    full_copy(SOURCE, DESTINATION)


if __name__ == '__main__':
    main()
