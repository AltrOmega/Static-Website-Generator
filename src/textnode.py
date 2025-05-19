from enum import Enum
from htmlnode import LeafNode
from typing import Tuple, List

class PatternLiteral:
    def __init__(self, *args):
        self.patterns: Tuple[str] = args
        self.starts = []
        self.ends = []

        for pattern in self.patterns:
            split: list = pattern.split('%')
            if '' in split:
                count = split.count('')
                if len(split) != count:
                    raise ValueError("Missing closing pattern in PatternLiteral definition.")
                return
            
            self.starts.append(split[0])
            self.ends.append( (*split[1:],) )





class TextType(Enum):
    TEXT = PatternLiteral('%')
    BOLD = PatternLiteral('**%**','__%__')
    ITALIC = PatternLiteral('*%*','_%_')
    CODE = PatternLiteral('`%`',)
    IMAGE = PatternLiteral('![%](%)',) # Todo: couses an error pls fix
    LINK = PatternLiteral('[%](%)',)

            



def extract_pattern(text: str, text_type: TextType):
    pattern_literal = text_type.value
    if pattern_literal.starts == []: return []

    #print(f'\ntext: ["{text}"]')
    i = None 
    open_pattern_index = None
    open_text_index = None
    for i in range(len(pattern_literal.starts)):
        start = pattern_literal.starts[i]

        open_pattern_index = text.find(start)
        if open_pattern_index != -1:
            open_text_index = open_pattern_index + len(start)
            break
    if open_pattern_index == -1:
        return []
    global_open_pattern_index = open_pattern_index
    global_close_pattern_index = 0
    extract = []
    end = '' 
    #print(f"\no[{open_pattern_index}:{text[open_pattern_index]}] ; [{open_text_index}:{text[open_text_index]}]")
    for j in range(len(pattern_literal.ends[i])):
        end = pattern_literal.ends[i][j]

        close_text_index = text.find(end, open_text_index)
        if close_text_index == -1: 
            raise ValueError(f"Given text is a missing closing pattern. ;{text}")
        global_close_pattern_index += close_text_index

        capture = text[open_text_index:close_text_index]
        extract.append(capture)

        #print(f"c[{close_text_index-1}:{text[close_text_index-1]}] ; [{close_pattern_index-1}:{text[close_pattern_index-1]}]")
        #print(f'capture: ["{capture}"]')
        text = text[close_text_index:]

        # will probably need to adjust the indexes here slightly
        open_pattern_index = 0 
        open_text_index = len(end)

    
    return (extract, global_open_pattern_index, global_close_pattern_index + len(end))





class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str=None, children=None):
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
        #TextNode(TEXT, TEXT_TYPE, URL)
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

