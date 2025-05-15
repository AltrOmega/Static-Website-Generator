from textnode import TextType, TextNode, extract_pattern
from typing import List
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6





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





def markdown_to_blocks(markdown: str):
    split: List[str] = markdown.split('\n\n')
    split = list(filter(lambda x: x != '', split))
    return list(map(lambda x: x.strip(), split))





def block_to_block_type_extract(block: str):
    l = len(block)

    if l >= 2 and block[0] in ['1', '2', '3', '4', '5', '6'] and block [1] == '#':
        return BlockType.HEADING, block[2:]
    
    if l >= 6 and block[:3] == '```' and block[-3:] == '```':
        return BlockType.CODE, block[3:-3]
    
    every_line = block.split('\n')
    ye = True
    extract = []
    for line in every_line:
        if len(line) < 1 or line[0] != '>':
            ye = False
            break

        extract.append(line[1:])

    if ye == True:
        return BlockType.QUOTE, '\n'.join(extract)
    

    ye = True
    extract = []
    for line in every_line:
        if len(line) < 2 or line[:2] != '- ':
            ye = False
            break

        extract.append(line[2:])
    if ye == True:
        return BlockType.UNORDERED_LIST, '\n'.join(extract)
    

    ye = True
    i = 0
    extract = []
    for line in every_line:
        i+=1
        if len(line) < 2 or line[:2] != f'{i}.':
            ye = False
            break

        extract.append(line[2:])
    if ye == True:
        return BlockType.ORDERED_LIST, '\n'.join(extract)
    

    return BlockType.PARAGRAPH, block