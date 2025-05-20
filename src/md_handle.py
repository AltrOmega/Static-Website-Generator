from textnode import *
from htmlnode import *
from typing import List
from regex_helpers import *
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
    LIST_INDEX = 'li'
    UNDEFINED = None



class Block:
    def __init__(self, block_text: str = '', block_type=BlockType.UNDEFINED, inner_blocks=[]):
        self.text = block_text
        self.type = block_type
        self.inner_blocks = inner_blocks

    def __repr__(self):
        if self.inner_blocks == []:
            return f"{self.type} |>{self.text}<|"
        else:
            return f"{self.type} {self.inner_blocks}"
    
    def __eq__(self, other):
        return self.type == other.type and self.text == other.text and self.inner_blocks == other.inner_blocks



def markdown_to_code_blocks(markdown: str) -> List[Block]:
    regex_str = (r"(?:\n|^)```([\s\S]*?)\n```")
    regex = re.compile(regex_str, flags=re.MULTILINE | re.DOTALL)
    
    text: str = markdown
    out = []
    match_ = regex.search(text)
    split = None
    while match_ != None:
        split = text.split(match_.group(0), maxsplit=1)

        if split[0].strip() != '':
            out.append(Block(split[0], BlockType.UNDEFINED))

        out.append(Block(match_.group(1), BlockType.CODE))

        text = split[-1]
        match_ = regex.search(text)

    if split is not None and split[1].strip() != '':
        out.append(Block(split[1], BlockType.UNDEFINED))
    
    if len(out) == 0:
        return [Block(markdown, BlockType.UNDEFINED)]

    return out



def handle_headers(blocks: List[Block]):
    regex_str = r"(?:^|\n)(#{1,6}) (.*)"
    regex = re.compile(regex_str)
    out = []
    for block in blocks:
        if block.type != BlockType.UNDEFINED:
            out.append(block)
            continue
            
        match_ = regex.search(block.text)
        text = block.text
        split = None
        while match_ != None:
            split = text.split(match_.group(0), maxsplit=1)
            if split[0].strip() != '':
                out.append(Block(split[0], BlockType.UNDEFINED))

            header_type = BlockType.HEADING_1
            match len(match_.group(1)):
                case 2:
                    header_type = BlockType.HEADING_2
                case 3:
                    header_type = BlockType.HEADING_3
                case 4:
                    header_type = BlockType.HEADING_4
                case 5:
                    header_type = BlockType.HEADING_5
                case 6:
                    header_type = BlockType.HEADING_6

            out.append(Block(match_.group(2), header_type))

            text = split[-1]
            match_ = regex.search(text)

        #print(f"Final SPLIT: ;{split};")
        if split is not None and split[1].strip() != '':
            out.append(Block(split[1], BlockType.UNDEFINED))
        elif split is None and block.type == BlockType.UNDEFINED:
            out.append(block)

        
    return out



def handle_quotes(blocks : List[Block]):
    regex_str = r"(\n(?:>\s*(.*?)(?:\n|$))+)"
    regex = re.compile(regex_str, flags=re.MULTILINE)
    out = []
    for block in blocks:
        if block.type != BlockType.UNDEFINED:
            out.append(block)
            continue
            
        match_ = regex.search(block.text)
        text = block.text
        split = None
        while match_ != None:
            split = text.split(match_.group(0), maxsplit=1)

            if split[0].strip() != '':
                out.append(Block(split[0], BlockType.UNDEFINED))

            first = True
            extract = None
            lines = match_.group(0).split('\n')
            for line in lines:
                if line.startswith('> '):
                    if first:
                        extract = f"{line[2:]}"
                        first = False
                    else:
                        extract = f"{extract} {line[2:]}"

            
            out.append(Block(extract, BlockType.QUOTE))

            text = split[-1]
            match_ = regex.search(text)

        if split is not None and split[1].strip() != '':
            out.append(Block(split[1], BlockType.UNDEFINED))
        elif split is None and block.type == BlockType.UNDEFINED:
            out.append(block)
    return out



def handle_unordered_lists(blocks: List[Block]):
    out = []
    line = None
    for block in blocks:
        if block.type != BlockType.UNDEFINED:
            out.append(block)
            continue

        lines = block.text.split('\n')
        
        undefineds = []
        exctracts = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if not lines[i].startswith('- '):
                undefineds.append(lines[i])
                i+=1
                continue

            if undefineds != []:
                out.append(Block('\n'.join(undefineds), BlockType.UNDEFINED))
                undefineds = []
            while i < len(lines) and lines[i].startswith('- '):
                exctracts.append(lines[i][2:])
                i+=1
            
            out.append(Block('', BlockType.UNORDERED_LIST, 
                list(map(lambda x: Block(x.strip(), BlockType.LIST_INDEX), exctracts)))
            )
            exctracts = []

        temp = '\n'.join(undefineds)
        if undefineds != [] and temp.strip() != '':
            out.append(Block(temp, BlockType.UNDEFINED))
    '''
    if line is not None and line.strip() != '':
        out.append(Block(line, BlockType.UNDEFINED))
    elif line is None and block.type == BlockType.UNDEFINED:
        out.append(block)
    '''

    if out == []:
        return blocks
    return out
    


def handle_ordered_lists(blocks: List[Block]):
    regex = re.compile(r"^(\d+).(.*)$")
    out = []
    for block in blocks:
        if block.type != BlockType.UNDEFINED:
            out.append(block)
            continue

        lines = block.text.split('\n')
        
        undefineds = []
        exctracts = []
        i = 0
        while i < len(lines):
            if regex.search(lines[i]) == None:
                undefineds.append(lines[i])
                i+=1
                continue

            if undefineds != []:
                out.append(Block('\n'.join(undefineds), BlockType.UNDEFINED))
                undefineds = []
            match_ = regex.search(lines[i])
            j = 1
            #print(f"MATCH: {match_.group(1)}")
            while i < len(lines) and match_ != None and int(match_.group(1)) == j:
                exctracts.append(match_.group(2))
                j += 1
                i+=1
                if i < len(lines):
                    match_ = regex.search(lines[i])
            
            out.append(Block('', BlockType.ORDERED_LIST, 
                list(map(lambda x: Block(x.strip(), BlockType.LIST_INDEX), exctracts)))
            )
            exctracts = []

        temp = '\n'.join(undefineds)
        if undefineds != [] and temp.strip() != '':
            out.append(Block(temp, BlockType.UNDEFINED))

    if out == []:
        return blocks
    return out
    


def undefined_to_paragraph(block: Block):
    if block.type == BlockType.UNDEFINED:
        return Block(block.text, BlockType.PARAGRAPH)
    return block

def undefined_to_paragraphs(blocks: List[Block]):
    return list(map(lambda x: undefined_to_paragraph(x), blocks))




def markdown_to_bloks(markdown: str) -> List[Block]:
    blocks = markdown_to_code_blocks(markdown)
    blocks = handle_headers(blocks)
    blocks = handle_quotes(blocks)
    blocks = handle_unordered_lists(blocks)
    blocks = handle_ordered_lists(blocks)
    blocks = undefined_to_paragraphs(blocks)
    return blocks


def block_to_html_node(block: Block):
    if block.type not in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        return LeafNode(block.type.value, block.text)
    else:
        return ParentNode(block.type.value, list(map(lambda x: block_to_html_node(x), block.inner_blocks)))

def blocks_to_html_node(blocks: List[Block]):
    children = list(map(lambda x: block_to_html_node(x), blocks))
    return ParentNode('div', children)





# Todo: start here, write unit tests for this function
def markdown_to_html_node(markdown: str):
    blocks = markdown_to_bloks(markdown)
    return blocks_to_html_node(blocks)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type, content = block_to_block_type_extract(block)
        if type == BlockType.HEADING_1:
            return content
    raise ValueError("Given markdown has no h1 header to extract the title from.")