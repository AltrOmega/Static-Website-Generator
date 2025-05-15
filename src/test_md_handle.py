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
            ("1# this is a header", (BlockType.HEADING, " this is a header")),
            ("```this is a code block```", (BlockType.CODE, "this is a code block")),
            ("- this is a \n- unordered list", (BlockType.UNORDERED_LIST, "this is a \nunordered list")),
            ("1. this is a \n2. ordered list", (BlockType.ORDERED_LIST, " this is a \n ordered list")),
        ]

        for test in tests:
            self.assertEqual(block_to_block_type_extract(test[0]), test[1])

if __name__ == "__main__":
    unittest.main()
