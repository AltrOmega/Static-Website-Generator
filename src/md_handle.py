from textnode import TextType, TextNode, extract_pattern
from typing import List
import re


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splat = node.text.split(delimiter, maxsplit=2)
        if len(splat) != 3:
            new_nodes.append(node)
            break

        if splat[0] != '':
            new_nodes.append(TextNode(splat[0], TextType.TEXT))
        
        new_nodes.append(TextNode(splat[1], text_type))
        new_nodes.extend(split_nodes_delimiter([TextNode(splat[2], TextType.TEXT)], delimiter, text_type))

    return new_nodes



def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)

def extract_markdown_image(text):
    return re.findall(r"!\[.*?\]\(.*?\)", text)


def split_nodes_image(old_nodes):
    new_nodes: List[TextNode] = []
    for node in old_nodes:

        extract = extract_markdown_image(node.text)
        if node.text_type != TextType.TEXT or extract is None or len(extract) == 0:
            new_nodes.append(node)
            continue

        print(f"[{extract[0]}]")
        splat = node.text.split(extract[1], maxsplit=1)
        if len(splat) != 2:
            new_nodes.append(node)
            break

        if splat[0] != '':
            new_nodes.append(TextNode(splat[0], TextType.TEXT))


        perc_ext = perc_extract(extract[1], TextType.IMAGE)
        new_nodes.append(TextNode(perc_ext[0], TextType.IMAGE, perc_ext[1]))
        if splat[1] != '':
            new_nodes.extend(split_nodes_image([TextNode(splat[1], TextType.TEXT)]))

    return new_nodes

def split_nodes_by_type(old_nodes: List[TextNode], text_type: TextType):
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        extract = extract_pattern(node.text, text_type)

        if extract == []:
            new_nodes.append(node)
            break
        
        contents = extract[0]
        open_index = extract[1]
        close_index = extract[2]
        new_nodes.append(TextNode(node.text[:open_index], TextType.TEXT))

        url = None
        if len(contents) > 1:
            url = contents[1]
        this = split_nodes_by_type
        new_nodes.extend( this( [TextNode(contents[0], text_type, url)], text_type ) )
        new_nodes.extend( this( [TextNode(node.text[close_index:], TextType.TEXT)], text_type ) )

    return new_nodes