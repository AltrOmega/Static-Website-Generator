from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = ('%',)
    BOLD = ('**%**','__%__')
    ITALIC = ('*%*','_%_')
    CODE = ('`%`',)
    LINK = ('[%](%)',)
    IMAGE = ('![%](%)',)

def perc_extract(text: str, text_type: TextType):
    if '%' in text_type.value: return text
    ret = []
    for pattern in text_type.value:
        splits = pattern.split('%')
        if text.find(splits[0]) != 0:
            continue
        
        for split in splits:
            split_begin = text.find(split)
            split_end = split_begin+len(split)

            before_txt = text[:split_begin]
            text = text[split_end:]
            if before_txt != '':
                ret.append(before_txt)

    return ret



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

