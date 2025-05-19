from textnode import TextType, TextNode, extract_pattern, text_node_to_html_node
from htmlnode import *
from typing import List
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'p'
    HEADING_1 = 'h1'
    HEADING_2 = 'h2'
    HEADING_3 = 'h3'
    HEADING_4 = 'h4'
    HEADING_5 = 'h5'
    HEADING_6 = 'h6'
    CODE = 'code'
    QUOTE = 'blockquote'
    UNORDERED_LIST = 'ul'
    ORDERED_LIST = 'ol'






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
    split: List[str] = re.split(r'\n\s*\n', markdown)
    split = list(filter(lambda x: x != '', split))
    ret = list(map(lambda x: x.strip(), split))
    return ret





def block_to_block_type_extract(block: str):
    l = len(block)

    if l >= 2 and block[0] == '#':
        if l >= 7 and block[:7] == '###### ':
            return BlockType.HEADING_6, block[7:]
        if l >= 6 and block[:6] == '##### ':
            return BlockType.HEADING_5, block[6:]
        if l >= 5 and block[:5] == '#### ':
            return BlockType.HEADING_4, block[5:]
        if l >= 4 and block[:4] == '### ':
            return BlockType.HEADING_3, block[4:]
        if l >= 3 and block[:3] == '## ':
            return BlockType.HEADING_2, block[3:]

        return BlockType.HEADING_1, block[2:]
    
    if l >= 6 and block[:3] == '```' and block[-3:] == '```':
        return BlockType.CODE, block[3:-3].lstrip('\n')
    
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





def markdown_to_html_node(markdown: str):

    def helper(type, content):
        text_nodes = text_to_textnodes(content)
        html_nodes = list(map(lambda text_node: text_node_to_html_node(text_node), text_nodes))
        return ParentNode(type.value, html_nodes, None)

    blocks = markdown_to_blocks(markdown)
    print(f"blocks: |||{blocks}|||")
    children = []
    for block in blocks:
        if block == '': continue
        type, content = block_to_block_type_extract(block)
        if content == '': continue
        print(f"type: |||{type}|||\ncontent: |||{content}|||")
        #content = content.strip()
        if type != BlockType.CODE:
            # next line is a temp test remove/change later
            content = ' '.join(content.split('\n'))
            children.append(helper(type, content))
        else:
            html_node = [LeafNode('code', content)]
            children.append(ParentNode('pre', html_node, None))

    return ParentNode('div', children)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type, content = block_to_block_type_extract(block)
        if type == BlockType.HEADING_1:
            return content
    raise ValueError("Given markdown has no h1 header to extract the title from.")