import unittest
from textnode import TextNode, TextType
from md_handle import *

class TestTextNode(unittest.TestCase):
    def test_markdown_to_code_blocks(self):
        tests = [
            ("```code\n```end", [ 
                Block("code", BlockType.CODE),
                Block("end", BlockType.UNDEFINED)
            ]),

            ("start\n```code\n```", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code", BlockType.CODE)
            ]),

            ("start\n```code\n```\nend", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code", BlockType.CODE),
                Block("\nend", BlockType.UNDEFINED),
            ]),

            ("start\n```code\n```\nend\nnewline", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code", BlockType.CODE),
                Block("\nend\nnewline", BlockType.UNDEFINED),
            ]),

            ("start\n```code'''code_ception'''code\n```end\nnewline", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code'''code_ception'''code", BlockType.CODE),
                Block("end\nnewline", BlockType.UNDEFINED),
            ]),

            ("start\n```code\n```\nend\n```more code\n```\nnewline", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code", BlockType.CODE),
                Block("\nend", BlockType.UNDEFINED),
                Block("more code", BlockType.CODE),
                Block("\nnewline", BlockType.UNDEFINED),
            ]),

            ("start\n```code\n```\nend\n```more code\n```\n```even more ```code```\n```", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code", BlockType.CODE),
                Block("\nend", BlockType.UNDEFINED),
                Block("more code", BlockType.CODE),
                Block("even more ```code```", BlockType.CODE),
            ]),

            ("start\n```code\n```\nsome more", [ 
                Block("start", BlockType.UNDEFINED),
                Block("code", BlockType.CODE),
                Block("\nsome more", BlockType.UNDEFINED),
            ]),

            ("pass", [ 
                Block("pass", BlockType.UNDEFINED),
            ]),
        ]

        for test in tests:
            out = markdown_to_code_blocks(test[0])
            self.assertListEqual(out, test[1])



    def test_handle_header(self):
        tests = [
            ("# h1", [ 
                Block("h1", BlockType.HEADING_1)
            ]),

            ("\n## h2\n\n", [ 
                Block("h2", BlockType.HEADING_2)
            ]),

            ("\n## h2\n\nafter", [ 
                Block("h2", BlockType.HEADING_2),
                Block("\n\nafter", BlockType.UNDEFINED),
            ]),

            ("## h2\n\nafter", [ 
                Block("h2", BlockType.HEADING_2),
                Block("\n\nafter", BlockType.UNDEFINED),
            ]),

            ("## h2\n### h3", [ 
                Block("h2", BlockType.HEADING_2),
                Block("h3", BlockType.HEADING_3)
            ]),

            ("\nbefore\n## h2\n### h3\n after", [ 
                Block("\nbefore", BlockType.UNDEFINED),
                Block("h2", BlockType.HEADING_2),
                Block("h3", BlockType.HEADING_3),
                Block("\n after", BlockType.UNDEFINED),
            ]),

            ("pass", [ 
                Block("pass", BlockType.UNDEFINED),
            ]),
        ]

        for test in tests:
            out = handle_headers([Block(test[0], BlockType.UNDEFINED)])
            self.assertListEqual(out, test[1])



    def test_handle_quotes(self):
        tests = [
            ("\n> quote", [ 
                Block("quote", BlockType.QUOTE)
            ]),

            ("\n some random text \n> quote\n some random text", [ 
                Block("\n some random text ", BlockType.UNDEFINED),
                Block("quote", BlockType.QUOTE),
                Block(" some random text", BlockType.UNDEFINED),
            ]),

            ("\n some random text \n> quote\n> next line in the same quote\n some random text", [ 
                Block("\n some random text ", BlockType.UNDEFINED),
                Block("quote next line in the same quote", BlockType.QUOTE),
                Block(" some random text", BlockType.UNDEFINED),
            ]),

            ("\n some random text \n> q> uote\n> next line in the same quote\n some> random text", [ 
                Block("\n some random text ", BlockType.UNDEFINED),
                Block("q> uote next line in the same quote", BlockType.QUOTE),
                Block(" some> random text", BlockType.UNDEFINED),
            ]),

            ("\n some random text \n> quote\n> next line in the same quote\n some random text\n> another quote", [ 
                Block("\n some random text ", BlockType.UNDEFINED),
                Block("quote next line in the same quote", BlockType.QUOTE),
                Block(" some random text", BlockType.UNDEFINED),
                Block("another quote", BlockType.QUOTE),
            ]),

            ("pass", [ 
                Block("pass", BlockType.UNDEFINED),
            ]),
        ]

        for test in tests:
            out = handle_quotes([Block(test[0], BlockType.UNDEFINED)])
            self.assertListEqual(out, test[1])


    def test_handle_unordered_lists(self):
        tests = [
            ("- index", [ 
                Block('', BlockType.UNORDERED_LIST, [Block('index', BlockType.LIST_INDEX)])
            ]),

            ("- index\n- index2", [ 
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)])
            ]),

            ("- -index\n- index2- ", [ 
                Block('', BlockType.UNORDERED_LIST, [
                    Block('-index', BlockType.LIST_INDEX),
                    Block('index2-', BlockType.LIST_INDEX)])
            ]),

            ("- index\n- index2\n\n- index3", [ 
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)]),
                Block('', BlockType.UNDEFINED),
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("- index\n- index2\nsome text\n- index3", [ 
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)]),
                Block('some text', BlockType.UNDEFINED),
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("- index\n- index2\nsome\ntext\n- index3", [ 
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)]),
                Block('some\ntext', BlockType.UNDEFINED),
                Block('', BlockType.UNORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("pass", [ 
                Block("pass", BlockType.UNDEFINED),
            ]),
        ]

        for test in tests:
            out = handle_unordered_lists([Block(test[0], BlockType.UNDEFINED)])
            #print(f"-OUTPUT: {out}")
            self.assertListEqual(out, test[1])



    def test_handle_ordered_lists(self):
        tests = [
            ("1. index", [ 
                Block('', BlockType.ORDERED_LIST, [Block('index', BlockType.LIST_INDEX)])
            ]),

            ("1. index\n2. index2", [ 
                Block('', BlockType.ORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)])
            ]),

            ("1. -index\n2. index2- ", [ 
                Block('', BlockType.ORDERED_LIST, [
                    Block('-index', BlockType.LIST_INDEX),
                    Block('index2-', BlockType.LIST_INDEX)])
            ]),

            ("1. index\n2. index2\n\n1. index3", [ 
                Block('', BlockType.ORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)]),
                Block('', BlockType.UNDEFINED),
                Block('', BlockType.ORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("1. index\n2. index2\nsome text\n1. index3", [ 
                Block('', BlockType.ORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)]),
                Block('some text', BlockType.UNDEFINED),
                Block('', BlockType.ORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("1. index\n2. index2\nsome\ntext\n1. index3", [ 
                Block('', BlockType.ORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX),
                    Block('index2', BlockType.LIST_INDEX)]),
                Block('some\ntext', BlockType.UNDEFINED),
                Block('', BlockType.ORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("1. index\n1. index2\nsome\ntext\n1. index3", [ 
                Block('', BlockType.ORDERED_LIST, [
                    Block('index', BlockType.LIST_INDEX)]),

                Block('', BlockType.ORDERED_LIST, [
                    Block('index2', BlockType.LIST_INDEX)]),

                Block('some\ntext', BlockType.UNDEFINED),

                Block('', BlockType.ORDERED_LIST, [
                    Block('index3', BlockType.LIST_INDEX)]),
            ]),

            ("pass", [ 
                Block("pass", BlockType.UNDEFINED),
            ]),
        ]

        for test in tests:
            #print(f"\n---TEST---:{test[0]}:---")
            out = handle_ordered_lists([Block(test[0], BlockType.UNDEFINED)])
            #print(f"\nOUTPUT: ;{out}; :END")
            self.assertListEqual(out, test[1])



    def test_markdown_to_blocks(self):
        tests = [
            (
"""
# head
``` baller
```
among us
""",[
    Block('head', BlockType.HEADING_1),
    Block(' baller', BlockType.CODE),
    Block('\namong us\n', BlockType.PARAGRAPH),
]),
            (
"""
###### head
``` baller
```
among us
> Who
> tucha
> my
> Spagett

amonus

# head2
- unone
- untwo

1. 1
2. 2
1. uno
""",[
    Block('head', BlockType.HEADING_6),
    Block(' baller', BlockType.CODE),
    Block('\namong us', BlockType.PARAGRAPH),
    Block('Who tucha my Spagett', BlockType.QUOTE),
    Block('\namonus\n', BlockType.PARAGRAPH),
    Block('head2', BlockType.HEADING_1),
    Block('', BlockType.UNORDERED_LIST, [
        Block('unone', BlockType.LIST_INDEX),
        Block('untwo', BlockType.LIST_INDEX),
    ]),
    Block('', BlockType.PARAGRAPH),
    Block('', BlockType.ORDERED_LIST, [
        Block('1', BlockType.LIST_INDEX),
        Block('2', BlockType.LIST_INDEX),
    ]),
    Block('', BlockType.ORDERED_LIST, [
        Block('uno', BlockType.LIST_INDEX),
    ]),
]),
            (
"""
among us
> Who
> tucha
# head 1
```
> my
> Spagett
```
more amonus
""",[
    Block('\namong us', BlockType.PARAGRAPH),
    Block('Who tucha', BlockType.QUOTE),
    Block('head 1', BlockType.HEADING_1),
    Block('\n> my\n> Spagett', BlockType.CODE),
    Block('\nmore amonus\n', BlockType.PARAGRAPH),
])
        ]

        for test in tests:
            #print(f"\n---Test---")
            out = markdown_to_bloks(test[0])
            self.assertListEqual(out, test[1])



    def test_blocks_to_html(self):
        tests = [
            ([
                Block('among us', BlockType.PARAGRAPH)
            ], ParentNode('div', [
                LeafNode('p', 'among us'),
            ])),

            ([
                Block('among us', BlockType.PARAGRAPH),
                Block('code', BlockType.CODE),
                Block('', BlockType.ORDERED_LIST, [Block('one', BlockType.LIST_INDEX)]),
            ], ParentNode('div', [
                LeafNode('p', 'among us'),
                LeafNode('code', 'code'),
                ParentNode('ol', [LeafNode('li', 'one')]),
            ])),

            ([
            ], ParentNode('div', [
            ])),

        ]

        for test in tests:
            self.assertEqual(blocks_to_html_node(test[0]), test[1])


if __name__ == "__main__":
    unittest.main()
