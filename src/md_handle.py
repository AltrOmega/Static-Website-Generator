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
    def __init__(self, block_text: str, block_type=BlockType.UNDEFINED):
        self.text = block_text
        self.type = block_type

    def __repr__(self):
        return f"{self.type} |>{self.text}<|"
    
    def __eq__(self, other):
        return self.type == other.type and self.text == other.text



def markdown_to_code_blocks(markdown: str) -> List[Block]:
    regex_str = (r"(?:\n|^)```([\s\S]*?)\n```")
    regex = re.compile(regex_str, flags=re.MULTILINE | re.DOTALL)
    
    text: str = markdown
    out = []
    match_ = regex.search(text)
    while match_ != None:
        split = text.split(match_.group(0), maxsplit=1)

        if split[0].strip() != '':
            out.append(Block(split[0], BlockType.UNDEFINED))

        out.append(Block(match_.group(1), BlockType.CODE))

        if split[1].strip() != '':
            out.append(Block(split[1], BlockType.UNDEFINED))
        # Should not be appending split[1] untill its out of the loop
        # just asighn to text todo: fix and add unittest that faill if you dont


        text = split[-1]
        match_ = regex.search(text)
    
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

        if split[1].strip() != '':
            out.append(Block(split[1], BlockType.UNDEFINED))
    return out



def markdown_to_bloks(markdown: str) -> List[Block]:
    blocks = markdown_to_code_blocks(markdown)
    blocks = handle_headers(blocks)
    # Todo: first fixt the todo in markdown_to_code_blocks then continue here

    return blocks





'''
class LineType(Enum): # probably no need for the extra space after deliminator, since will strip it either way
    HEADING_6 = strings_begin_to_regexes('###### %', '######%')
    HEADING_5 = strings_begin_to_regexes('##### %', '#####%')
    HEADING_4 = strings_begin_to_regexes('#### %', '####%')
    HEADING_3 = strings_begin_to_regexes('### %', '###%')
    HEADING_2 = strings_begin_to_regexes('## %', '##%')
    HEADING_1 = strings_begin_to_regexes('# %', '#%')
    QUOTE = strings_begin_to_regexes('> %', '>%')
    UNOREDERED_LIST = strings_begin_to_regexes('- %', '-%')
    ORDERED_LIST = (re.compile(r"^\d+\.\s?(.*$)"),)# ("number. %", "number.%")
    CODE = strings_begin_to_regexes('``` %', '```%')

def markdown_to_lines(markdown: str):
    lines = []
    for line in markdown.split('\n'):
        found = False
        for line_type in LineType:
            for regex in line_type.value:
                match_ = regex.search(line)
                if match_:
                    lines.append( (line_type, line, match_.group(1)) )
                    found = True
                    break
            if found:
                break
        if not found:
            lines.append( (None, line, ''))
            found = False
    return lines

def lines_to_blocks(lines: Tuple[LineType|None, str, str]):
    blocks = []
    in_code_block = False
    order_num = 0
    for i in range(len(lines)):
        line = lines[i]
        line_type, whole, capture = line

        if in_code_block:
            pass

        match line_type:
            case LineType.CODE:
                

            case None:
                blocks.append((BlockType.PARAGRAPH, whole))

            case LineType.HEADING_1:
                blocks.append((BlockType.HEADING_1, capture.strip()))
            case LineType.HEADING_2:
                blocks.append((BlockType.HEADING_2, capture.strip()))
            case LineType.HEADING_3:
                blocks.append((BlockType.HEADING_3, capture.strip()))
            case LineType.HEADING_4:
                blocks.append((BlockType.HEADING_4, capture.strip()))
            case LineType.HEADING_5:
                blocks.append((BlockType.HEADING_5, capture.strip()))
            case LineType.HEADING_6:
                blocks.append((BlockType.HEADING_6, capture.strip()))

        


def markdown_to_blocks(markdown: str):
    split: List[str] = re.split(r'\n\s*\n', markdown)
    split = list(filter(lambda x: x != '', split))
    ret = list(map(lambda x: x.strip(), split))
    return ret
'''           




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