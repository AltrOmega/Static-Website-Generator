import unittest
from textnode import TextNode, TextType
from md_handle import *

class TestTextNode(unittest.TestCase):
    def _test_markdown_to_lines(self):
        tests = [
            ("# aye", [ (LineType.HEADING_1, "# aye", "aye") ]),
            ("#aye", [(LineType.HEADING_1, "#aye", "aye")]),
            ("> aye\n>m8", [(LineType.QUOTE, "> aye", "aye"), (LineType.QUOTE, ">m8", "m8")]),
            ("> aye\n```m8", [(LineType.QUOTE, "> aye", "aye"), (LineType.CODE, "```m8", "m8")]),
            ("######aye\n```m8\n", [(LineType.HEADING_6, "######aye", "aye"), (LineType.CODE, "```m8", "m8"), (None, "", "")]),
            ("######aye\n```m8\n ", [(LineType.HEADING_6, "######aye", "aye"), (LineType.CODE, "```m8", "m8"), (None, " ", "")]),
            (" \nsome text\n ", [(None, " ", ""), (None, "some text", ""), (None, " ", "")]),
            ("1. one\n2.two\n3.  three", [(LineType.ORDERED_LIST, "1. one", "one"), (LineType.ORDERED_LIST, "2.two", "two"), (LineType.ORDERED_LIST, "3.  three", " three")]),
        ]

        for test in tests:
            #print("Test 0: " + test[0])
            #print("out: " + str(markdown_to_lines(test[0])))
            self.assertListEqual(markdown_to_lines(test[0]), test[1])

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

            ("## h2\n### h3", [ 
                Block("h2", BlockType.HEADING_2),
                Block("h3", BlockType.HEADING_3)
            ]),
        ]

        for test in tests:
            out = handle_headers([Block(test[0], BlockType.UNDEFINED)])
            self.assertListEqual(out, test[1])


    def _test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def _test_block_to_block_type_extract(self):
        tests = [
            ("this is a paragraph", (BlockType.PARAGRAPH, "this is a paragraph")),
            ("# this is a h1 header", (BlockType.HEADING_1, "this is a h1 header")),
            ("## this is a h2 header", (BlockType.HEADING_2, "this is a h2 header")),
            ("### this is a h3 header", (BlockType.HEADING_3, "this is a h3 header")),
            ("#### this is a h4 header", (BlockType.HEADING_4, "this is a h4 header")),
            ("##### this is a h5 header", (BlockType.HEADING_5, "this is a h5 header")),
            ("###### this is a h6 header", (BlockType.HEADING_6, "this is a h6 header")),
            ("```this is a code block```", (BlockType.CODE, "this is a code block")),
            ("- this is a \n- unordered list", (BlockType.UNORDERED_LIST, "this is a \nunordered list")),
            ("1. this is a \n2. ordered list", (BlockType.ORDERED_LIST, " this is a \n ordered list")),
        ]

        for test in tests:
            self.assertEqual(block_to_block_type_extract(test[0]), test[1])


    def _test_codeblock(self):
        tests = [
            ("""
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"),
            ("""```This is text that _should_ remain
the **same** even with inline stuff
``` """, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"),
            ("""
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"),
        ]

        for test in tests:
            self.assertEqual(markdown_to_html_node(test[0]).to_html(), test[1])

    def _test_paragraphs(self):
        tests = [
            ("""

paragraph
and its newline

""", "<div><p>paragraph and its newline</p></div>"), # dear god this looks disgusting
            ("""

paragraph
and its newline
            
and another paragraph

""", "<div><p>paragraph and its newline</p><p>and another paragraph</p></div>"),
            ("""paragraph
and its newline
            


and another paragraph
""", "<div><p>paragraph and its newline</p><p>and another paragraph</p></div>"),
            ("""This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
""", "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"),
            ("""error?: This is **bolded** paragraph
text in a __p__
ta*g h*ere

`This is another paragraph` with _italic_ text and `code` here
""", "<div><p>error?: This is <b>bolded</b> paragraph text in a <b>p</b> ta<i>g h</i>ere</p><p><code>This is another paragraph</code> with <i>italic</i> text and <code>code</code> here</p></div>"),

# ---------------------------
        ]

        for test in tests:
            print(f"\n\n\nTESTING; {test[0]} ;TESTING")
            self.assertEqual(markdown_to_html_node(test[0]).to_html(), test[1])



    def _test_extract_title(self):
        tests = [
            ("# header", "header"),
            ("## h2\n\n# header", "header"),
            ("this is a paragraph i think\n\n# header\n\nhere is another", "header"),
        ]

        for test in tests:
            self.assertEqual(extract_title(test[0]), test[1])



if __name__ == "__main__":
    unittest.main()
