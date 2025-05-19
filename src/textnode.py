from enum import Enum
from htmlnode import LeafNode
from typing import List
from regex_helpers import *

"""
Those patterns are for readability.
They will get turn to a non greedy regex pattern where
% is a capture everything.

The patterns will get searched in the order they are defined in the enum.
"""
class TextType(Enum):
    IMAGE = strings_to_regexes('![%](%)')
    LINK = strings_to_regexes('[%](%)')
    BOLD = strings_to_regexes('**%**','__%__')
    ITALIC = strings_to_regexes('*%*','_%_')
    CODE = strings_to_regexes('`%`')
    TEXT = () 

def extract_pattern(text: str, text_type: TextType):
    for pattern in text_type.value:
        match_ = pattern.search(text)
        if match_:
            return match_.groups(), match_.start(0), match_.end(0)
    return None





class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode('b', text_node.text)

        case TextType.ITALIC:
            return LeafNode('i', text_node.text)

        case TextType.CODE:
            return LeafNode('code', text_node.text)

        case TextType.LINK:
            return LeafNode('a', text_node.text, props={'href': text_node.url})

        case TextType.IMAGE:
            return LeafNode('img', None, props={'src': text_node.url, 'alt': text_node.text})





def split_nodes_by_type(old_nodes: List[TextNode], text_type: TextType):
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        extract = extract_pattern(node.text, text_type)

        if extract == None:
            new_nodes.append(node)
            continue
        
        contents, open_index, close_index = extract

        new_nodes.append(TextNode(node.text[:open_index], TextType.TEXT))

        url = None
        if len(contents) > 1:
            url = contents[1]
        new_nodes.append( TextNode(contents[0], text_type, url) )
        new_nodes.extend( split_nodes_by_type( [TextNode(node.text[close_index:], TextType.TEXT)], text_type ) )

    return new_nodes





def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    for text_type in TextType:
        nodes = split_nodes_by_type(nodes, text_type)

    return nodes
