from textnode import TextType, TextNode, extract_pattern
from typing import List
import re

def split_nodes_by_type(old_nodes: List[TextNode], text_type: TextType):
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        extract = extract_pattern(node.text, text_type)

        if extract == []:
            new_nodes.append(node)
            continue
        
        contents = extract[0]
        open_index = extract[1]
        close_index = extract[2]
        new_nodes.append(TextNode(node.text[:open_index], TextType.TEXT))

        url = None
        if len(contents) > 1:
            url = contents[1]
        this = split_nodes_by_type
        new_nodes.append( TextNode(contents[0], text_type, url) )
        new_nodes.extend( this( [TextNode(node.text[close_index:], TextType.TEXT)], text_type ) )

    return new_nodes





def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    for text_type in TextType:
        nodes = split_nodes_by_type(nodes, text_type)

    return nodes
