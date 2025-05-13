from textnode import TextType, TextNode
from typing import List


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




def old_split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        d_count = node.text.count(delimiter)

        if d_count == 0:
            new_nodes.append(node)
            continue

        if d_count % 2 != 0:
            raise ValueError("Wrong ammount of delimiters.")


        text = node.text

        splat = text.split(delimiter, maxsplit=2)
        while len(splat) != 3:

            if splat[0] != '':
                new_nodes.append(TextNode(splat[0], TextType.TEXT))

            new_nodes.append(TextNode(splat[1], text_type))
            splat = splat[2]
    
    new_nodes.append(TextNode(splat[2], TextType.TEXT))
    return new_nodes

        
            
        
        