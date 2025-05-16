import unittest
from textnode import TextNode, TextType
from md_handle import *

class TestTextNode(unittest.TestCase):
    def _test_split_nodes_delimiter(self):
        test = TextNode("amogus **ballder** sus", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([test], '**', TextType.BOLD),[
            TextNode("amogus ", TextType.TEXT),
            TextNode("ballder", TextType.BOLD),
            TextNode(" sus", TextType.TEXT),
        ])

    def test_split_nodes_by_type(self):
        tests = [
            ("this is **bolded** text", TextType.BOLD, [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is __bolded__ text", TextType.BOLD, [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is _italic_ text", TextType.ITALIC, [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is `some ` `code` text", TextType.CODE, [
                TextNode("this is ", TextType.TEXT),
                TextNode("some ", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]),
        ]

        for test in tests:
            self.assertListEqual(
                split_nodes_by_type(
                    [TextNode(test[0], TextType.TEXT)], test[1]
                    ),
                test[2]
            )

    def test_text_to_textnodes(self):
        tests = [
            ("this is **bolded** text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is __bolded__ text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is _italic_ text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is `some ` `code` text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("some ", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is `some code` and **bold** text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
        ]

        for test in tests:
            self.assertListEqual(
                text_to_textnodes( test[0] ),
                test[1]
            )


    def test_markdown_to_blocks(self):
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

    def test_block_to_block_type_extract(self):
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


    def test_codeblock(self):
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

    def test_paragraphs(self):
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
            ("""This is **bolded** paragraph
text in a __p__
ta*g h*ere

`This is another paragraph` with _italic_ text and `code` here
""", "<div><p>This is <b>bolded</b> paragraph text in a <b>p</b> ta<i>g h</i>ere</p><p><code>This is another paragraph</code> with <i>italic</i> text and <code>code</code> here</p></div>"),
        ]
        

        for test in tests:
            self.assertEqual(markdown_to_html_node(test[0]).to_html(), test[1])



if __name__ == "__main__":
    unittest.main()
